'''
System tests for `jenkinsapi.jenkins` module.
'''
import unittest
from jenkinsapi.build import Build
from jenkinsapi_tests.test_utils.random_strings import random_string
from jenkinsapi_tests.systests.base import BaseSystemTest, EMPTY_JOB_CONFIG


class JobTests(BaseSystemTest):

    def test_create_job(self):
        job_name = 'create_%s' % random_string()
        self.jenkins.create_job(job_name, EMPTY_JOB_CONFIG)
        self.assertJobIsPresent(job_name)

    def test_enable_disable_job(self):
        job_name = 'create_%s' % random_string()
        self.jenkins.create_job(job_name, EMPTY_JOB_CONFIG)
        self.assertJobIsPresent(job_name)

        j = self.jenkins[job_name]
        j.invoke(block=True) # run this at least once

        j.disable()
        self.assertEquals(j.is_enabled(), False, 'A disabled job is reporting incorrectly')
        j.enable()
        self.assertEquals(j.is_enabled(), True, 'An enabled job is reporting incorrectly')

    def test_get_job_and_update_config(self):
        job_name = 'config_%s' % random_string()
        self.jenkins.create_job(job_name, EMPTY_JOB_CONFIG)
        self.assertJobIsPresent(job_name)
        config = self.jenkins[job_name].get_config()
        self.assertEquals(config.strip(), EMPTY_JOB_CONFIG.strip())
        self.jenkins[job_name].update_config(EMPTY_JOB_CONFIG)

    def test_invoke_job(self):
        job_name = 'create_%s' % random_string()
        job = self.jenkins.create_job(job_name, EMPTY_JOB_CONFIG)
        job.invoke()

    def test_get_jobs_list(self):
        job1_name = 'first_%s' % random_string()
        job2_name = 'second_%s' % random_string()

        self._create_job(job1_name)
        self._create_job(job2_name)
        job_list = self.jenkins.get_jobs_list()
        self.assertEqual([job1_name, job2_name], job_list)

    def test_delete_job(self):
        job1_name = 'delete_me_%s' % random_string()

        self._create_job(job1_name)
        self.jenkins.delete_job(job1_name)
        self.assertJobIsAbsent(job1_name)

    def test_rename_job(self):
        job1_name = 'A__%s' % random_string()
        job2_name = 'B__%s' % random_string()

        self._create_job(job1_name)
        self.jenkins.rename_job(job1_name, job2_name)
        self.assertJobIsAbsent(job1_name)
        self.assertJobIsPresent(job2_name)

    def test_copy_job(self):

        template_job_name = 'TPL%s' % random_string()
        copied_job_name = 'CPY%s' % random_string()

        self._create_job(template_job_name)
        self.jenkins.copy_job(template_job_name, copied_job_name)
        self.assertJobIsPresent(template_job_name)
        self.assertJobIsPresent(copied_job_name)

class NodeTests(BaseSystemTest):
    """
    """

    # def test_get_node_dict(self):
    #     self.assertEqual(self.jenkins.get_node_dict(), {
    #         'master': 'http://localhost:8080/computer/master/api/python/'})

if __name__ == '__main__':
    unittest.main()
