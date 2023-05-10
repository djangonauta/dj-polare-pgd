from django.utils import log


class UsuarioFormatter(log.ServerFormatter):

    def format(self, record):
        record.current_user = 'Anônimo'
        request = getattr(record, 'request', None)
        if request is not None:
            record.current_user = request.user.username

        return super().format(record)
