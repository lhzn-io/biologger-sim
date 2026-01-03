-- Copyright (c) 2025-2026 Long Horizon Observatory
-- Licensed under the Apache License, Version 2.0. See LICENSE file for details.

-- Use folder name to build extension name and tag.
local ext = get_current_extension_info()

project_ext (ext)

-- Link only those files and folders into the extension target directory
repo_build.prebuild_link {
    { "data", ext.target_dir.."/data" },
    { "layouts", ext.target_dir.."/layouts" },
    { "whoimpg", ext.target_dir.."/whoimpg" },
}
