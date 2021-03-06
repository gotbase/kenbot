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
import abc
import copy

import kenbot.backtesting as kenbot_backtesting
import kenbot.api as kenbot_api
import kenbot_commons.constants as commons_constants
import kenbot_commons.logging as bot_logging
import kenbot_commons.tentacles_management as tentacles_management
import kenbot_commons.tests.test_config as test_config
import kenbot_evaluators.evaluators as evaluators
import kenbot_tentacles_manager.api as tentacles_manager_api
import kenbot_tentacles_manager.constants as tentacles_manager_constants
import kenbot_trading.api as trading_api
import tests.test_utils.config as test_utils_config
import tentacles.Evaluator.Strategies as Strategies
import tentacles.Trading.Mode as Mode

DEFAULT_SYMBOL = "ICX/BTC"
DATA_FILE_PATH = "tests/static/"


class AbstractStrategyTest(kenbot_backtesting.AbstractBacktestingTest, abc.ABC):
    __metaclass__ = abc.ABCMeta

    def initialize(self, strategy_evaluator_class, trading_mode_class=Mode.DailyTradingMode, config=None):
        self.logger = bot_logging.get_logger(self.__class__.__name__)
        self.config = test_config.load_test_config() if config is None else config
        # remove fees
        self.config[commons_constants.CONFIG_SIMULATOR][commons_constants.CONFIG_SIMULATOR_FEES][
            commons_constants.CONFIG_SIMULATOR_FEES_TAKER] = 0
        self.config[commons_constants.CONFIG_SIMULATOR][commons_constants.CONFIG_SIMULATOR_FEES][
            commons_constants.CONFIG_SIMULATOR_FEES_MAKER] = 0
        self.strategy_evaluator_class = strategy_evaluator_class
        self.trading_mode_class = trading_mode_class
        self.tentacles_setup_config = test_utils_config.load_test_tentacles_config()
        self._update_tentacles_config(strategy_evaluator_class, trading_mode_class)

    def _handle_results(self, independent_backtesting, profitability):
        exchange_manager_ids = kenbot_api.get_independent_backtesting_exchange_manager_ids(independent_backtesting)
        for exchange_manager in trading_api.get_exchange_managers_from_exchange_ids(exchange_manager_ids):
            _, run_profitability, _, market_average_profitability, _ = trading_api.get_profitability_stats(
                exchange_manager)
            actual = round(run_profitability, 3)
            # uncomment this print for building tests
            # print(f"results: rounded run profitability {actual} market profitability: {market_average_profitability}"
            #       f" expected: {profitability} [result: {actual ==  profitability}]")
            assert actual == profitability

    async def _run_backtesting_with_current_config(self, data_file_to_use):
        config_to_use = copy.deepcopy(self.config)
        independent_backtesting = kenbot_api.create_independent_backtesting(config_to_use,
                                                                             self.tentacles_setup_config,
                                                                             [data_file_to_use],
                                                                             "")
        await kenbot_api.initialize_and_run_independent_backtesting(independent_backtesting, log_errors=False)
        await kenbot_api.join_independent_backtesting(independent_backtesting)
        return independent_backtesting

    def _update_tentacles_config(self, strategy_evaluator_class, trading_mode_class):
        default_evaluators = strategy_evaluator_class.get_default_evaluators(self.tentacles_setup_config)
        to_update_config = {}
        tentacles_activation = tentacles_manager_api.get_tentacles_activation(self.tentacles_setup_config)
        for tentacle_class_name in tentacles_activation[tentacles_manager_constants.TENTACLES_EVALUATOR_PATH]:
            if commons_constants.CONFIG_WILDCARD not in default_evaluators and tentacle_class_name in default_evaluators:
                to_update_config[tentacle_class_name] = True
            elif tentacles_management.get_class_from_string(tentacle_class_name, evaluators.StrategyEvaluator,
                                                            Strategies,
                                                            tentacles_management.evaluator_parent_inspection) is not None:
                to_update_config[tentacle_class_name] = False
            elif commons_constants.CONFIG_WILDCARD not in default_evaluators:
                to_update_config[tentacle_class_name] = False
        for tentacle_class_name in tentacles_activation[tentacles_manager_constants.TENTACLES_TRADING_PATH]:
            to_update_config[tentacle_class_name] = False
        # Add required elements if missing
        to_update_config.update({evaluator: True for evaluator in default_evaluators})
        to_update_config[strategy_evaluator_class.get_name()] = True
        to_update_config[trading_mode_class.get_name()] = True
        tentacles_manager_api.update_activation_configuration(self.tentacles_setup_config, to_update_config, False,
                                                              add_missing_elements=True)
