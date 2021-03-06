# cython: language_level=3
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

cimport kenbot.backtesting.kenbot_backtesting as kenbot_backtesting


cdef class IndependentBacktesting:
    cdef list forced_time_frames

    cdef public dict kenbot_origin_config
    cdef public dict backtesting_config
    cdef public object tentacles_setup_config
    cdef public list backtesting_files

    cdef object logger
    cdef object join_backtesting_timeout

    cdef public str data_file_path
    cdef public dict symbols_to_create_exchange_classes
    cdef public double risk
    cdef public dict starting_portfolio
    cdef public dict fees_config
    cdef public bint stopped

    cdef public object post_backtesting_task

    cdef public kenbot_backtesting.kenbotBacktesting kenbot_backtesting

    cpdef bint is_in_progress(self)
    cpdef double get_progress(self)
    cpdef void log_report(self)

    cdef void _post_backtesting_start(self)
    cdef void _init_default_config_values(self)
    cdef dict _get_exchanges_report(self, str reference_market, object trading_mode)
    cdef void _log_trades_history(self, object exchange_manager, str exchange_name)
    cdef void _log_symbol_report(self, str symbol, object exchange_manager, object min_time_frame)
    cdef void _log_global_report(self, object exchange_manager)
    cdef void _adapt_config(self)
    cdef str _find_reference_market(self)
    cdef void _add_config_default_backtesting_values(self)
    cdef void _add_crypto_currencies_config(self)
