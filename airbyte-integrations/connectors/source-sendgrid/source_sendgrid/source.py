#
# Copyright (c) 2021 Airbyte, Inc., all rights reserved.
#

from asyncio import streams
from typing import Any, List, Mapping, Tuple

from airbyte_cdk.models import SyncMode
from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.streams.http.auth import TokenAuthenticator

from .streams import (  # MessagesTemplate,
    Blocks,
    Bounces,
    Campaigns,
    Contacts,
    GlobalSuppressions,
    InvalidEmails,
    Lists,
    Messages,
    MessagesDetails,
    Scopes,
    Segments,
    SingleSends,
    SpamReports,
    StatsAutomations,
    SuppressionGroupMembers,
    SuppressionGroups,
    Templates,
)


class SourceSendgrid(AbstractSource):

    # @staticmethod
    # def _get_authenticator(config: Mapping[str, Any]): 
    #     return TokenAuthenticator(config["apikey"])

    def check_connection(self, logger, config) -> Tuple[bool, any]:
        try:
            authenticator = TokenAuthenticator(config["apikey"])
            scopes_gen = Scopes(authenticator=authenticator).read_records(sync_mode=SyncMode.full_refresh)
            next(scopes_gen)
            return True, None
        except Exception as error:
            return False, f"Unable to connect to Sendgrid API with the provided credentials - {error}"

    def streams(self, config: Mapping[str, Any]) -> List[Stream]:
        authenticator = TokenAuthenticator(config["apikey"])

        messages = Messages(authenticator=authenticator, start_time=config["start_time"])
        streams = [
            Lists(authenticator=authenticator),
            Campaigns(authenticator=authenticator),
            Contacts(authenticator=authenticator),
            StatsAutomations(authenticator=authenticator),
            Segments(authenticator=authenticator),
            SingleSends(authenticator=authenticator),
            Templates(authenticator=authenticator),
            messages,
            MessagesDetails(authenticator=authenticator,start_time=config["start_time"], parent=messages),
            # MessagesTemplate(authenticator=authenticator),
            GlobalSuppressions(authenticator=authenticator, start_time=config["start_time"]),
            SuppressionGroups(authenticator=authenticator),
            SuppressionGroupMembers(authenticator=authenticator),
            Blocks(authenticator=authenticator, start_time=config["start_time"]),
            Bounces(authenticator=authenticator, start_time=config["start_time"]),
            InvalidEmails(authenticator=authenticator, start_time=config["start_time"]),
            SpamReports(authenticator=authenticator, start_time=config["start_time"]),
        ]

        return streams
