from werkzeug.exceptions import Conflict, BadRequest, NotFound, InternalServerError

class HttpConflictError(Conflict):
    description = "A requisição não pôde ser completada devido a um conflito com o estado atual do recurso, como duplicidade de entrada."

class HttpBadRequestError(BadRequest):
    description = "A requisição não pôde ser completada devido a parâmetros inválidos ou dados malformados."

class HttpNotFoundError(NotFound):
    description = "O recurso solicitado não foi encontrado."

class HttpInternalServerError(InternalServerError):
    description = "O servidor encontrou uma condição inesperada que o impediu de atender à requisição."