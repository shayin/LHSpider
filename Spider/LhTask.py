# -*- coding: utf-8 -*-

import enum

class LhTask(enum.Enum):

    TASK_RUNNING = "task_running"

    TASK_FETCH = "task_fetch"
    TASK_PARSE = "task_parse"
    TASK_SAVE = "task_save"

    TASK_NOT_FETCH = "task_not_fetch"
    TASK_NOT_PARSE = "task_not_parse"
    TASK_NOT_SAVE = "task_not_save"

    TASK_ERROR = "task_error"
    TASK_FAIL = "task_fail"
