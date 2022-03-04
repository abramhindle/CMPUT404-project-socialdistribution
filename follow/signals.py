from django.dispatch import Signal

request_create = Signal()
request_reject = Signal()
request_cancel = Signal()
request_accept = Signal()
follow_remove = Signal()
