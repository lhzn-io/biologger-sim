# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.
#
# Portions Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.
import carb.settings
import omni.kit.app
from omni.kit.test import AsyncTestCase


class TestAppStartup(AsyncTestCase):
    def app_startup_time(self, test_id: str) -> float:
        """Get startup time - send to nvdf"""
        startup_time = float(omni.kit.app.get_app().get_time_since_start_s())
        print(f"App Startup time: {startup_time}")
        return startup_time

    def app_startup_warning_count(self, test_id: str) -> tuple[int, int]:
        """Get the count of warnings during startup - send to nvdf"""
        warning_count = 0
        error_count = 0
        log_file_path = carb.settings.get_settings().get("/log/file")
        with open(log_file_path) as file:
            for line in file:
                if "[Warning]" in line:
                    warning_count += 1
                elif "[Error]" in line:
                    error_count += 1

        print(f"App Startup Warning count: {warning_count}")
        print(f"App Startup Error count: {error_count}")
        return warning_count, error_count

    async def test_l1_app_startup_time(self) -> None:
        """Get startup time - send to nvdf"""
        for _ in range(60):
            await omni.kit.app.get_app().next_update_async()

        self.app_startup_time(self.id())
        self.assertTrue(True)

    async def test_l1_app_startup_warning_count(self) -> None:
        """Get the count of warnings during startup - send to nvdf"""
        for _ in range(60):
            await omni.kit.app.get_app().next_update_async()

        self.app_startup_warning_count(self.id())
        self.assertTrue(True)
