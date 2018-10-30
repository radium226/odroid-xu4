#!/usr/bin/env python

from pathlib import Path
from tempfile import mkdtemp

from .context import Context

from system.tools.ansible import Ansible
from system.tools.git import Git

def provision(prompt):
    context = Context()
    print(context.config)
    repo_folder_path = Path(mkdtemp())
    Git.clone(context.config["provision"]["git_repo_url"], repo_folder_path)
    provisioning_folder_path = repo_folder_path / context.config["provision"]["folder_path"]
    host_name = context.config["provision"]["host_name"]
    inventory_file_path = provisioning_folder_path / context.config["provision"]["inventory_file_path"]
    vault_password_file_path = context.vault_password_file_path
    Ansible(inventory_file_path, vault_password_file_path).run_playbook(provisioning_folder_path / context.config["provision"]["playbook_file_path"], limit=[host_name], local=True)
