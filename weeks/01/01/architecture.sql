-- Version and storage mode used by this lab.
SELECT current_version() AS starrocks_version, @@run_mode AS run_mode;

-- Which node accepts queries?
SHOW FRONTENDS;

-- Which node stores rows and runs the work here?
SHOW BACKENDS;

-- Are any separate compute nodes (CNs) registered?
SHOW COMPUTE NODES;
