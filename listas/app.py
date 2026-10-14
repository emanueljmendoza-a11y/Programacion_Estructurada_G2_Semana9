import uuid
from pathlib import Path

from flask import Flask, jsonify, render_template, request, url_for
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB por foto

MAX_CAPACITY = 20
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
UPLOAD_DIR = Path(app.static_folder) / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# ---------- Excepciones ----------
class StackError(Exception):
    """Error base de la pila, con su código HTTP."""
    status = 400


class StackNotConfiguredError(StackError):
    status = 409


class StackFullError(StackError):
    status = 409


class StackEmptyError(StackError):
    status = 409


# ---------- Lógica de la pila ----------
class Stack:
    """Pila (LIFO) con capacidad máxima. Guarda cualquier tipo de elemento."""

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise StackError("La capacidad debe ser mayor que cero.")
        self._capacity = capacity
        self._items: list[dict] = []

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def items(self) -> list[dict]:
        return list(self._items)  # copia: protege el estado interno

    def __len__(self) -> int:
        return len(self._items)

    def is_empty(self) -> bool:
        return not self._items

    def is_full(self) -> bool:
        return len(self._items) >= self._capacity

    def push(self, item: dict) -> None:
        if self.is_full():
            raise StackFullError("La pila está llena.")
        self._items.append(item)

    def pop(self) -> dict:
        if self.is_empty():
            raise StackEmptyError("La pila está vacía.")
        return self._items.pop()

    def peek(self) -> dict:
        if self.is_empty():
            raise StackEmptyError("La pila está vacía.")
        return self._items[-1]


# Estado en memoria (suficiente para una práctica de clase).
stack: Stack | None = None


# ---------- Manejo de fotos ----------
def photo_url(item: dict) -> str:
    return url_for("static", filename=f"uploads/{item['file']}")


def public(item: dict) -> dict:
    """Datos de la foto que sí se envían al navegador."""
    return {"name": item["name"], "url": photo_url(item)}


def save_photo(file) -> dict:
    """Valida y guarda la foto subida. Devuelve su registro."""
    raw_name = file.filename or ""
    ext = Path(raw_name).suffix.lower().lstrip(".")
    if ext not in ALLOWED_EXTENSIONS:
        raise StackError("Formato no permitido. Usa PNG, JPG, GIF o WEBP.")
    if not (file.mimetype or "").startswith("image/"):
        raise StackError("El archivo seleccionado no es una imagen.")

    stored_name = f"{uuid.uuid4().hex}.{ext}"  # nombre único y seguro
    file.save(UPLOAD_DIR / stored_name)
    display_name = secure_filename(raw_name) or f"foto.{ext}"
    return {"file": stored_name, "name": display_name}


def delete_photo(item: dict) -> None:
    (UPLOAD_DIR / item["file"]).unlink(missing_ok=True)


def clear_uploads() -> None:
    """Borra fotos que hayan quedado de ejecuciones anteriores."""
    for path in UPLOAD_DIR.iterdir():
        if path.is_file() and path.suffix.lower().lstrip(".") in ALLOWED_EXTENSIONS:
            path.unlink(missing_ok=True)


def discard_stack() -> None:
    """Elimina la pila actual y sus fotos."""
    global stack
    if stack is not None:
        for item in stack.items:
            delete_photo(item)
    stack = None


# ---------- Utilidades de respuesta ----------
def get_stack() -> Stack:
    if stack is None:
        raise StackNotConfiguredError("Primero define el tamaño de la pila.")
    return stack


def snapshot() -> dict:
    """Estado actual de la pila, listo para enviarlo como JSON."""
    if stack is None:
        return {"configured": False}
    return {
        "configured": True,
        "capacity": stack.capacity,
        "items": [public(item) for item in stack.items],  # de la base al tope
        "size": len(stack),
        "is_empty": stack.is_empty(),
        "is_full": stack.is_full(),
    }


def response(message: str | None = None, **extra):
    return jsonify({"message": message, "state": snapshot(), **extra})


# ---------- Manejo de errores ----------
@app.errorhandler(StackError)
def handle_stack_error(error: StackError):
    return jsonify({"error": str(error)}), error.status


@app.errorhandler(RequestEntityTooLarge)
def handle_too_large(_error):
    return jsonify({"error": "La foto supera el límite de 5 MB."}), 413


# ---------- Rutas ----------
@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/stack")
def api_state():
    return response()


@app.post("/api/stack")
def api_create():
    global stack
    data = request.get_json(silent=True) or {}
    try:
        capacity = int(data.get("capacity"))
    except (TypeError, ValueError):
        raise StackError("Introduce un número entero válido.")
    if not 1 <= capacity <= MAX_CAPACITY:
        raise StackError(f"El tamaño debe estar entre 1 y {MAX_CAPACITY}.")
    discard_stack()
    stack = Stack(capacity)
    return response(f"Pila creada con capacidad {capacity}."), 201


@app.delete("/api/stack")
def api_reset():
    discard_stack()
    return response("Pila reiniciada.")


@app.post("/api/stack/push")
def api_push():
    current = get_stack()
    if current.is_full():  # se valida antes de guardar el archivo
        raise StackFullError("La pila está llena.")

    file = request.files.get("photo")
    if file is None or not file.filename:
        raise StackError("Selecciona una foto para apilar.")

    item = save_photo(file)
    current.push(item)
    return response(f"Foto «{item['name']}» agregada a la pila."), 201


@app.post("/api/stack/pop")
def api_pop():
    item = get_stack().pop()
    delete_photo(item)
    return response(f"Se eliminó la foto «{item['name']}» del tope.")


@app.get("/api/stack/peek")
def api_peek():
    item = get_stack().peek()
    return response(f"El tope de la pila es «{item['name']}».", value=public(item))


@app.get("/api/stack/is-empty")
def api_is_empty():
    empty = get_stack().is_empty()
    return response("La pila está vacía." if empty else "La pila NO está vacía.")


@app.get("/api/stack/size")
def api_size():
    return response(f"La pila tiene {len(get_stack())} foto(s).")


if __name__ == "__main__":
    clear_uploads()
    app.run(debug=True)  # debug solo para desarrollo