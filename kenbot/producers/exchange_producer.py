#  gotbase kenbot
#  Copyright (c) gotbase, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import kenbot_commons.enums as common_enums
import kenbot_commons.constants as common_constants

import kenbot_trading.api as trading_api
import kenbot_trading.kenbot_channel_consumer as trading_channel_consumer

import kenbot.channels as kenbot_channel


class ExchangeProducer(kenbot_channel.kenbotChannelProducer):
    def __init__(self, channel, kenbot, backtesting, ignore_config=False):
        super().__init__(channel)
        self.kenbot = kenbot
        self.ignore_config = ignore_config

        self.backtesting = backtesting
        self.exchange_manager_ids = []

    async def start(self):
        for exchange_name in self.kenbot.config[common_constants.CONFIG_EXCHANGES]:
            if self.kenbot.config[common_constants.CONFIG_EXCHANGES][exchange_name].get(
                    common_constants.CONFIG_ENABLED_OPTION, True):
                await self.create_exchange(exchange_name, self.backtesting)

    async def stop(self):
        for exchange_manager in trading_api.get_exchange_managers_from_exchange_ids(self.exchange_manager_ids):
            await trading_api.stop_exchange(exchange_manager)

    async def create_exchange(self, exchange_name, backtesting):
        await self.send(bot_id=self.kenbot.bot_id,
                        subject=common_enums.kenbotChannelSubjects.CREATION.value,
                        action=trading_channel_consumer.kenbotChannelTradingActions.EXCHANGE.value,
                        data={
                            trading_channel_consumer.kenbotChannelTradingDataKeys.TENTACLES_SETUP_CONFIG.value:
                                self.kenbot.tentacles_setup_config,
                            trading_channel_consumer.kenbotChannelTradingDataKeys.MATRIX_ID.value:
                                self.kenbot.evaluator_producer.matrix_id,
                            trading_channel_consumer.kenbotChannelTradingDataKeys.BACKTESTING.value: backtesting,
                            trading_channel_consumer.kenbotChannelTradingDataKeys.EXCHANGE_CONFIG.value:
                                self.kenbot.config,
                            trading_channel_consumer.kenbotChannelTradingDataKeys.EXCHANGE_NAME.value: exchange_name,
                        })
