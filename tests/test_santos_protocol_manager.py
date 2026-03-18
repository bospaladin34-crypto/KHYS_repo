import os
import tempfile
import shutil
import unittest

from santos_protocol_manager import (MODULES, REGISTRY_PATH, AUDIT_PATH,
                                    load_registry, save_registry, create_module,
                                    collect_status, load_audit, log_event)


class TestSantosProtocolManager(unittest.TestCase):
    def setUp(self):
        self.repo_dir = os.path.dirname(__file__)
        self.original_cwd = os.getcwd()
        os.chdir(os.path.join(self.original_cwd, '..'))

        # Backup existing registry/audit if present
        self.registry_backup = None
        self.audit_backup = None
        if os.path.exists(REGISTRY_PATH):
            self.registry_backup = REGISTRY_PATH + '.bak'
            shutil.copy2(REGISTRY_PATH, self.registry_backup)
        if os.path.exists(AUDIT_PATH):
            self.audit_backup = AUDIT_PATH + '.bak'
            shutil.copy2(AUDIT_PATH, self.audit_backup)

        # Reset registry
        if os.path.exists(REGISTRY_PATH):
            os.remove(REGISTRY_PATH)
        if os.path.exists(AUDIT_PATH):
            os.remove(AUDIT_PATH)

    def tearDown(self):
        if self.registry_backup:
            shutil.move(self.registry_backup, REGISTRY_PATH)
        elif os.path.exists(REGISTRY_PATH):
            os.remove(REGISTRY_PATH)

        if self.audit_backup:
            shutil.move(self.audit_backup, AUDIT_PATH)
        elif os.path.exists(AUDIT_PATH):
            os.remove(AUDIT_PATH)

        os.chdir(self.original_cwd)

    def test_registry_and_audit(self):
        modules = load_registry()
        self.assertIsInstance(modules, list)

        created = create_module('tests_temp_module', dependencies=['Santos_Protocol_Core'])
        self.assertTrue(created.endswith('.logic'))

        status = collect_status()
        self.assertIn('modules', status)

        audit = load_audit()
        self.assertTrue(any(item['action'] == 'create_module' for item in audit))

        log_event('test_event', {'foo': 'bar'})
        audit2 = load_audit()
        self.assertTrue(any(item['action'] == 'test_event' for item in audit2))

        # Cleanup created module file
        temp_path = os.path.join(os.path.dirname(__file__), '..', created)
        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == '__main__':
    unittest.main()
