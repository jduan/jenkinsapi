'''
System tests for `jenkinsapi.jenkins` module.
'''
import os
import time
import shutil
import random
import tempfile
import unittest
from jenkinsapi_tests.test_utils.random_strings import random_string
from jenkinsapi_tests.systests.base import BaseSystemTest

JOB_CONFIG = """
<?xml version='1.0' encoding='UTF-8'?>
<project>
  <actions/>
  <description>A build that explores the wonderous possibilities of parameterized builds.</description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <hudson.model.ParametersDefinitionProperty>
      <parameterDefinitions>
        <hudson.model.StringParameterDefinition>
          <name>B</name>
          <description>B, like buzzing B.</description>
          <defaultValue></defaultValue>
        </hudson.model.StringParameterDefinition>
      </parameterDefinitions>
    </hudson.model.ParametersDefinitionProperty>
  </properties>
  <scm class="hudson.scm.NullSCM"/>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers class="vector"/>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command>ping -c 1 localhost | tee out.txt
cat $A &gt; a.txt
cat $B &gt; b.txt</command>
    </hudson.tasks.Shell>
  </builders>
  <publishers>
    <hudson.tasks.ArtifactArchiver>
      <artifacts></artifacts>
      <latestOnly>false</latestOnly>
    </hudson.tasks.ArtifactArchiver>
    <hudson.tasks.Fingerprinter>
      <targets></targets>
      <recordBuildArtifacts>false</recordBuildArtifacts>
    </hudson.tasks.Fingerprinter>
  </publishers>
  <buildWrappers/>
</project>""".strip()

class TestParameterizedBuilds(BaseSystemTest):

    def test_invoke_job_parameterized(self):

        param_B = random_string()

        job_name = 'create_%s' % random_string()
        job = self.jenkins.create_job(job_name, JOB_CONFIG)
        job.invoke(block=True, build_params={ 'B':param_B})

        b = job.get_last_build()
        while b.is_running():
            time.sleep(0.25)

        artifacts = b.get_artifact_dict()
        self.assertIsInstance(artifacts, dict)

        artA = artifacts['A.txt']
        artB = artifacts['B.txt']

        # TODO: Actually verify the download


if __name__ == '__main__':
    unittest.main()
