from django.conf import settings
from django.utils.encoding import smart_str

from celery.task import Task
from celery.registry import tasks

from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol

from website.apps.thrift.service import ClousureService
from website.apps.utils.settings import STATUS_PROCESSED, STATUS_FAILED

class ResourceCompile(Task):
    def run(self, resource, compiler_config=[]):
        logger = ResourceCompile.get_logger()

        try:
            transport = TSocket.TSocket(settings.THRIFT_SERVER, settings.THRIFT_PORT)
            transport = TTransport.TFramedTransport(transport)
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            client = ClousureService.Client(protocol)

            transport.open()
            result = client.compileJS(
                resource.uuid,
                smart_str(resource.source),
                compiler_config
            )

            resource.compiler_errors = result.compilerErrors
            resource.compiler_warnings = result.compilerWarnings
            resource.status = STATUS_PROCESSED

            if result.compilerErrors:
                resource.status = STATUS_FAILED

            if not len(result.compilerErrors):
                resource.source_processed = result.sourceProcessed
                resource.source_map = result.sourceMap

            resource.save()
        except Exception, ex:
            logger.error(ex.message)
            resource.status = STATUS_FAILED
            resource.save()
            return False
        finally:
            transport.close()

        return True

tasks.register(ResourceCompile)
