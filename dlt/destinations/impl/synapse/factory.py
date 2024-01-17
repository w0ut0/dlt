import typing as t

from dlt.common.destination import Destination, DestinationCapabilitiesContext
from dlt.destinations.impl.synapse import capabilities

from dlt.destinations.impl.synapse.configuration import (
    SynapseCredentials,
    SynapseClientConfiguration,
)

if t.TYPE_CHECKING:
    from dlt.destinations.impl.synapse.synapse import SynapseClient


class synapse(Destination[SynapseClientConfiguration, "SynapseClient"]):
    spec = SynapseClientConfiguration

    def capabilities(self) -> DestinationCapabilitiesContext:
        return capabilities()    

    @property
    def client_class(self) -> t.Type["SynapseClient"]:
        from dlt.destinations.impl.synapse.synapse import SynapseClient

        return SynapseClient

    def __init__(
        self,
        credentials: t.Union[SynapseCredentials, t.Dict[str, t.Any], str] = None,
        create_indexes: bool = False,
        destination_name: t.Optional[str] = None,
        environment: t.Optional[str] = None,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(
            credentials=credentials,
            create_indexes=create_indexes,
            destination_name=destination_name,
            environment=environment,
            **kwargs,
        )
