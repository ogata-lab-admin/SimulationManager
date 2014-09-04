#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file SimulationManager.py
 @brief Test Component for Simulator
 @date $Date$


"""
import sys, yaml, os, traceback, subprocess, datetime, types
import time
sys.path.append(".")

VREP_RTC_PATH='localhost:2809/VREPRTC0.rtc'
SELF_RTC_PATH='localhost:2809/SimulationManager0.rtc'

# Import RTM module
import RTC
import OpenRTM_aist
import CORBA, CosNaming
from omniORB import any
# import rtctree
#sys.path.insert(1, os.path.join(rtctree.__path__[0], 'rtmidl'))
#import rtshell
#import OpenRTM__POA
#reload(OpenRTM__POA)
#from rtshell import rtresurrect

import Simulator_idl

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
import ssr, ssr__POA


# </rtc-template>

import Tkinter as tk

# This module's spesification
# <rtc-template block="module_spec">
simulatortest_spec = ["implementation_id", "SimulationManager", 
		 "type_name",         "SimulationManager", 
		 "description",       "Test Component for Simulator", 
		 "version",           "1.0.0", 
		 "vendor",            "ysuga_net", 
		 "category",          "Simulator", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "naming.format",    "%n.rtc",
	         "conf.default.simulation_setup_on_activated", "false",
		 "conf.default.fullpath_to_self", "localhost/SimulationManager0.rtc",
		 "conf.default.project",   "None",
		 "conf.default.rtsystem",   "None",
		 "conf.default.robots", "{}",
		 "conf.default.ranges", "{}",
		 "conf.default.cameras", "{}", 
		 "conf.default.sync_rtcs", "[]",
		 "conf.default.simulation_times", "0",
		 "conf.default.simulation_end_condition", "timespan",
                 "conf.default.simulation_end_timespan", "10.0",
                 "conf.default.simulation_end_rtcpath", "localhost/VREPRTC0.rtc",
		 "conf.default.simulation_start_on_activated", "false", 
		 "conf.default.simulation_setup_on_activated", "false", 
		 #Widget
		 "conf.__widget__.simulation_end_condition", "radio", 
		 "conf.__widget__.simulation_start_on_activated", "radio",
		 "conf.__widget__.simulation_setup_on_activated", "radio",
		 # Constraints
		 "conf.__constraints__.simulation_end_condition", "timespan,rtcdeactivated,rtcactivated,rtcerror",
		 "conf.__constraints__.simulation_start_on_activated", "true, false",
		 "conf.__constraints__.simulation_setup_on_activated", "true, false",
		 ""]
# </rtc-template>

##
# @class SimulationManager
# @brief Test Component for Simulator
# 
# 
class SimulationManager(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)


		"""
		"""
		self._simulatorPort = OpenRTM_aist.CorbaPort("simulator")

		

		"""
		"""
		self._simulator = OpenRTM_aist.CorbaConsumer(interfaceType=ssr.Simulator)

		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		
		self._fullpath_to_self = ["localhost/SimulationManager0.rtc"]
		self._project = ["[]"]
		self._rtsystem = ["[]"]
		self._robots = ["{}"]
		self._cameras = ["{}"]
		self._ranges = ["{}"]
		self._sync_rtcs = ["[]"]
		self._simulation_times = [1]
		self._simulation_end_condition = ["timespan"]
		self._simulation_end_timespan = [10.0]
		self._simulation_end_rtcpath = ["localhost/VREPRTC0.rtc"]
		self._simulation_start_on_activated = ["false"]
		self._simulation_setup_on_activated = ["false"]
		# </rtc-template>
		
		self._standalone = False
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		self.bindParameter("fullpath_to_self", self._fullpath_to_self, "localhost/SimulationManager0.rtc")
		self.bindParameter("project", self._project, "[]")
		self.bindParameter("rtsystem", self._rtsystem, "[]")
		self.bindParameter("robots", self._robots, "{}")
		self.bindParameter("cameras", self._cameras, "{}")
		self.bindParameter("ranges", self._ranges, "{}")
		self.bindParameter("sync_rtcs", self._sync_rtcs, "[]")
		self.bindParameter("simulation_times", self._simulation_times, "1")
		self.bindParameter("simulation_end_condition", self._simulation_end_condition, "timespan")
		self.bindParameter("simulation_end_timespan", self._simulation_end_timespan, "10.0")
		self.bindParameter("simulation_end_rtcpath", self._simulation_end_rtcpath, "localhost/VREPRTC0.rtc")
		self.bindParameter("simulation_start_on_activated", self._simulation_start_on_activated, "false")
		self.bindParameter("simulation_setup_on_activated", self._simulation_setup_on_activated, "false")
		# Set InPort buffers
		
		# Set OutPort buffers
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		self._simulatorPort.registerConsumer("Simulator", "ssr::Simulator", self._simulator)
		
		# Set CORBA Service Ports
		self.addPort(self._simulatorPort)

		self.root = None
		self._time = 0.0
		self._timeStep = 0.0
		self._simulation_turn = 0
		
		return RTC.RTC_OK
	
	#	##
	#	# 
	#	# The finalize action (on ALIVE->END transition)
	#	# formaer rtc_exiting_entry()
	#	# 
	#	# @return RTC::ReturnCode_t
	#
	#	# 
	#def onFinalize(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The startup action when ExecutionContext startup
	#	# former rtc_starting_entry()
	#	# 
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The shutdown action when ExecutionContext stop
	#	# former rtc_stopping_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The activated action (Active state entry action)
	#	# former rtc_active_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	# 
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	def onActivated(self, ec_id):
		flag = self._simulation_setup_on_activated[0]
		if flag == 'true' or flag == 'True' or flag == 'TRUE':
			return self.setup_simulation(ec_id)
		else:
			return RTC.RTC_OK

	def setup_simulation(self, ec_id):
		sys.stdout.write(' - Now Activating Simulation(ec_id=%s)....\n' % ec_id)
		if ec_id != 0:
			sys.stdout.write(' -- Extra Execution Context (Maybe synchronized in Simulator) is activated.\n')
			retval, self._timeStep = self._simulator._ptr().getSimulationTimeStep()
			retval, self._time = self._simulator._ptr().getSimulationTime()
			return RTC.RTC_OK

		for i in range(0, 20):
			sys.stdout.write('#')
			sys.stdout.flush()
			time.sleep(0.025)
			
		print ''
		sys.stdout.write(' - Staring activation routine\n')
		try:
			sys.stdout.write(' - Killing All Simulated RTCs\n')
			#
			#ret = self._simulator._ptr().killAllRobotRTC()
			#if not ret == ssr.RETVAL_OK:
			#	sys.stdout.write(' - Failed. ret=%s\n' % ret)
			#	return RTC.RTC_ERROR

			sys.stdout.write(' -- Waiting 0.5 seconds\n')
			for i in range(0, 20):
				sys.stdout.write('#')
				sys.stdout.flush()
				time.sleep(0.025)
				pass
		except Exception, e:
			sys.stdout.write(' -- Failed to killAllRTC\n')
			traceback.print_exc()
			return RTC.RTC_ERROR

		
		try:
			if not len(self._project[0].strip()) == 0 and self._project[0] != 'None' and self._project[0] != '[]':
				sys.stdout.write(' - Opening Project %s\n' % self._project[0])
				project_file = self._project[0]
				cwd = os.getcwd()
				full_path = os.path.join(cwd, project_file)
				if not os.path.isfile(full_path):
					full_path = project_file
				if not os.path.isfile(full_path):
					sys.stdout.write(' -- File not found:%s' % full_path)
					sys.stdout.write(' -- Skipping Open Project Process.\n')
					#return RTC.RTC_ERROR
				else:
					sys.stdout.write(' -- Loading Project : %s\n' % full_path)
					if not self._simulator._ptr().loadProject(full_path) == ssr.RETVAL_OK:
						sys.stdout.write(' -- Failed.')
						return RTC.RTC_ERROR

					sys.stdout.write(' -- Waiting 1 seconds\n')
					for i in range(0, 20):
						sys.stdout.write('#')
						sys.stdout.flush()
						time.sleep(0.05)
						pass
					pass
		except Exception, e:
			sys.stdout.write(' -- Failed to loadProject\n')
			traceback.print_exc()
			return RTC.RTC_ERROR
		sys.stdout.write('\n')

		try:
			robots = yaml.load(self._robots[0])
			if robots:
				for r, a in robots.items():
					sys.stdout.write(' - Spawning Robot: %s?%s\n' % (r, a))
					if not self._simulator._ptr().spawnRobotRTC(r, a) == ssr.RETVAL_OK:
						sys.stdout.write(' - Failed\n')
						#return RTC.RTC_ERROR
		except Exception, e:
			sys.stdout.write(' - Failed to spawn RTCs\n')
			traceback.print_exc()
			return RTC.RTC_ERROR
		try:
			ranges = yaml.load(self._ranges[0])
			if ranges:
				for r, a in ranges.items():
					sys.stdout.write(' - Spawning Range: %s?%s\n' % (r,a))
					if not self._simulator._ptr().spawnRangeRTC(r, a) == ssr.RETVAL_OK:
						sys.stdout.write(' - Failed\n')
						#return RTC.RTC_ERROR

		except Exception, e:
			sys.stdout.write(' - Failed to spawn RTCs\n')
			traceback.print_exc()
			return RTC.RTC_ERROR
		try:
			cameras = yaml.load(self._cameras[0])
			if cameras:
				for c, a in cameras.items():
					sys.stdout.write(' - Spawning Camera: %s?%s\n' % (c,a))
					if not self._simulator._ptr().spawnCameraRTC(c, a) == ssr.RETVAL_OK:
						sys.stdout.write(' - Failed\n')
						#return RTC.RTC_ERROR
		except Exception, e:
			sys.stdout.write(' - Failed to spawn RTCs\n')
			traceback.print_exc()
			return RTC.RTC_ERROR
		
		try:
			sys.stdout.write(' - Synchronize Request of SimulationManager(%s)\n' % self._fullpath_to_self[0])
			if not self._simulator._ptr().synchronizeRTC(self._fullpath_to_self[0]) == ssr.RETVAL_OK:
				sys.stdout.write(' -- Failed.\n')
				#return RTC.RTC_ERROR

			sync_rtcs = yaml.load(self._sync_rtcs[0])
                        if type(sync_rtcs) != types.ListType:
                                sync_rtcs = [sync_rtcs]
			if sync_rtcs:
				for r in sync_rtcs:
					sys.stdout.write(' - Synchronize Request for RTC(%s)\n' % r)
					if not self._simulator._ptr().synchronizeRTC(r) == ssr.RETVAL_OK:
						sys.stdout.write(' -- Failed\n')
						#return RTC.RTC_ERROR

		except Exception, e:
			sys.stdout.write(' -- Failed to synchronize RTCs\n')
			traceback.print_exc()
			return RTC.RTC_ERROR

		sys.stdout.write(' -- Waiting 1 seconds\n')
		for i in range(0, 20):
			sys.stdout.write('#')
			sys.stdout.flush()
			time.sleep(0.05)
		sys.stdout.write('\n')
		count = 0
		try:
			#if not len(self._rtsystem[0].strip()) == 0 and self._rtsystem[0] != '[]' and self._rtsystem[0] != 'None':
			while not len(self._rtsystem[0].strip()) == 0 and self._rtsystem[0] != '[]' and self._rtsystem[0] != 'None':
				try:
                                        
					sys.stdout.write(' - Building RT System with %s\n' % self._rtsystem[0])

					if sys.platform == 'win32':
						ret = subprocess.call(['rtresurrect.bat', self._rtsystem[0]])
					else:
						ret = subprocess.call(['rtresurrect', self._rtsystem[0]])
					sys.stdout.write(' -- rtresurrect == %s\n' % ret)
                                        if ret == 0:
                                                break
                                        sys.stdout.write(' -- rtresurrect failed. Retry...\n')
                                                
				except:
					sys.stdout.write(' -- rtresurrect failed. Retry...\n')
					traceback.print_exc()
				time.sleep(1.0)
				count = count + 1
				if count == 5:
                                        sys.stdout.write(' -- building system failed. But proceeding setup.....')
                                        break
		except Exception ,e:
			sys.stdout.write(' -- Failed to construct RTCs\n')
			traceback.print_exc()
			return RTC.RTC_ERROR

		sys.stdout.write(' -- Waiting 1 seconds\n')
		for i in range(0, 20):
			sys.stdout.write('#')
			sys.stdout.flush()
			time.sleep(0.05)
		sys.stdout.write('\n')

		try:
			if not len(self._rtsystem[0].strip()) == 0 and self._rtsystem[0] != '[]':
				try:
					sys.stdout.write(' - Starting RT System with %s\n' % self._rtsystem[0])

					if sys.platform == 'win32':
						ret = subprocess.call(['rtstart.bat', self._rtsystem[0]])
					else:
						ret = subprocess.call(['rtstart', self._rtsystem[0]])
					sys.stdout.write(' -- rtstart == %s\n' % ret)



				except:
					sys.stdout.write(' - rtstart failed. Retry...\n')
					traceback.print_exc()
				time.sleep(1.0)

		except Exception ,e:
			sys.stdout.write(' - Failed to start RTCs\n')
			traceback.print_exc()
			return RTC.RTC_ERROR

		try:
			print ' - simulation_start_on_activated : ', self._simulation_start_on_activated[0]
                        flag = self._simulation_start_on_activated[0]
			if flag == 'true' or flag == 'True' or flag == 'TRUE' :
				self._simulation_turn = 0
				print ' - Starting Simulation.' 
				if not self._simulator._ptr().start() == ssr.RETVAL_OK:
					return RTC.RTC_ERROR
		except Exception, e:
			sys.stdout.write(' - Failed to start Simulation\n');
			traceback.print_exc()
			return RTC.RTC_ERROR
		
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The deactivated action (Active state exit action)
	#	# former rtc_active_exit()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	def onDeactivated(self, ec_id):
		if ec_id != 0:
			sys.stdout.write(' - onDeactivated with ec_id=%s\n' % ec_id)
			return RTC.RTC_OK

		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The execution action that is invoked periodically
	#	# former rtc_active_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	def onExecute(self, ec_id):
		if ec_id != 0:
			sys.stdout.write(' - exec by %s\n' % ec_id)
			# "Synchronizing EC"
			if self._simulation_end_condition[0] == 'timespan':
				retval, current_time = self._simulator._ptr().getSimulationTime()
				self._time = self._time + self._timeStep
				print 'CurrentTime     = ', current_time
				print 'Calculated Time = ', self._time
			elif self._simulation_end_condition[0] == 'rtcdeactivated':
				pass
			elif self._simulation_end_condition[0] == 'rtcactivated':
				pass
			elif self._simulation_end_condition[0] == 'rtcerror':
				pass
			else:
				sys.stdout.write(' -- Error. Unknown End Condition (conf.default.simulation_end_condition=%s)\n' % self._simulation_end_condition)
				return RTC.RTC_ERROR
			pass
		else:
			if self._simulation_end_timespan[0] < self._time:
				print ' - Simulation Ends (', self._simulation_turn, '/', self._simulation_times[0]
				self._time = 0
				if self._simulation_turn < self._simulation_times[0]:
					self._simulator._ptr().stop()
					self._simulation_turn = self._simulation_turn + 1
					if self._simulation_turn < self._simulation_times[0]:
						for i in range(0, 5):
							print ' - Restarting Simulation ...',
							if self._simulator._ptr().start() == ssr.RETVAL_OK:
								print 'OK'
								break
							else:
								print 'Failed'
							if i == 4:
								print 'Error. Failed %s times.' % (i+1)
								return RTC.RTC_ERROR
							time.sleep(3)

			pass
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The aborting action when main logic error occurred.
	#	# former rtc_aborting_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The error action in ERROR state
	#	# former rtc_error_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The reset action that is invoked resetting
	#	# This is same but different the former rtc_init_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The state update action that is invoked after onExecute() action
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#

	#	#
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The action that is invoked when execution context's rate is changed
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK
	

	def on_start(self):
		self._simulator._ptr().start()

	def on_stop(self):
		self._simulator._ptr().stop()

	def on_proj_find(self):
		sys.stdout.write(' - Finding Project file')
		import tkFileDialog
		filename = tkFileDialog.askopenfilename()
		filename = filename.replace('/', '\\')
		cwd = os.getcwd()
		print ""
		if filename.startswith(cwd):
			filename = filename[len(cwd)+1:]
		if filename:
			self.loadEntryBuf.set(filename)
			self._projEntryBuffer.set(filename)

	def on_load(self):

		project_file = str(self.loadEntryBuf.get())
		full_path = os.path.join(os.getcwd(), project_file)
		if not os.path.isfile(full_path):
			full_path = project_file
		if not os.path.isfile(full_path):
			print 'File not found (%s)' % full_path
			return
		print 'Loading Project %s' % full_path
		print 'type = ', type(full_path)
		if not self._simulator._ptr().loadProject(full_path) == ssr.RETVAL_OK:
			print 'Failed to load (%s)' % full_path
			return
		print 'Success.'

	def on_save_conf(self):
		print 'Save configuration to current directory'
		ns, addr, port = self.get_self_rtc_paths()
		conf_dictionary = {
			'conf.default.fullpath_to_self': ns + '/' + addr, 
			'conf.default.project': self.loadEntryBuf.get(),
			'conf.default.rtsystem': self.rtsysNameEntryBuffer.get(),
			'conf.default.robots': self._confRobotsBuffer.get(),
			'conf.default.cameras': self._confCamerasBuffer.get(),
			'conf.default.ranges': self._confRangesBuffer.get(),
			'conf.default.sync_rtcs': self.synchRTCEntryBuffer.get(),
			'conf.default.simulation_start_on_activated' : True,
			'conf.default.simulation_setup_on_activated' : True,
			}

		conf_file_name = 'SimulationManager0.conf'
		saved_conf = {}
		backup_file_name = conf_file_name + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
		if os.path.isfile(conf_file_name):
			os.rename(conf_file_name, backup_file_name)
		if not os.path.isfile(conf_file_name):
			open(conf_file_name, 'w').close()

		"""
		with open(conf_file_name + '.bak', 'r') as fin:
			with open(conf_file_name, 'w') as fout:
				for line in fin:
					for key, value in conf_dictionary.items():
						if line.startswith(key):
							fout.write(key + ' : ' + value + '\n')
							saved_conf[key] = value
						else:
							fout.write(line)
				for key, value in conf_dictionary.items():
					if not key in saved_conf.keys():
						fout.write(key + ' : ' + value + '\n')
		"""
		fout = open(conf_file_name, 'w')
		for key, value in conf_dictionary.items():
			fout.write(key + ' : ' + str(value) + '\n')
		fout.close()
				
	def on_spawn_robot(self):
		self._simulator._ptr().spawnRobotRTC(self.robotEntryBuffer.get(), self.robotArgEntryBuffer.get())

	def on_spawn_range(self):
		self._simulator._ptr().spawnRangeRTC(self.rangeEntryBuffer.get(), self.rangeArgEntryBuffer.get())

	def on_spawn_camera(self):
		self._simulator._ptr().spawnCameraRTC(self.cameraEntryBuffer.get(), self.cameraArgEntryBuffer.get())

	def on_synch(self):
		rtcpath = self.synchRTCEntryBuffer.get()
		print rtcpath
		print type(rtcpath)
		if not len(rtcpath) == 0:
			if not self._simulator._ptr().synchronizeRTC(rtcpath) == ssr.RETVAL_OK:
				sys.stdout.write(' -- Failed')
				return
		pass

	def on_update(self):
		addr = VREP_RTC_PATH
		selfAddr = SELF_RTC_PATH

		clientNS = selfAddr.split('/')[0]
		clientAddr = selfAddr[:selfAddr.rfind(':')][len(clientNS)+1:]
		if clientNS.find(':') < 0: clientNS = clientNS+':2809'
		clientPortName = selfAddr.split(':')[1]
		hostNS = addr.split('/')[0]
		hostAddr   = addr[:addr.rfind(':')][len(hostNS)+1:]
		if hostNS.find(':') < 0: hostNS = hostNS+':2809'
		hostPortName   = addr.split(':')[1]

		robotRTCs  = {}
		rangeRTCs  = {}
		cameraRTCs = {}
		otherRTCs = {}
		try:
			clientCorbaNaming = OpenRTM_aist.CorbaNaming(OpenRTM_aist.Manager.instance().getORB(), clientNS)
			root_cxt = clientCorbaNaming.getRootContext()

			def parseContext(cxt_str, cxt):
				objs = []
				bindingList, bindingIterator = cxt.list(30)
				for b in bindingList:
					if b.binding_type == CosNaming.ncontext:
						child_cxt_str = b.binding_name[0].id + '.' + b.binding_name[0].kind + '/'
						objs = objs + [cxt_str + o for o in parseContext(child_cxt_str, cxt.resolve(b.binding_name))]
					elif b.binding_type == CosNaming.nobject:
						objs.append(cxt_str + b.binding_name[0].id + '.' + b.binding_name[0].kind)
				return objs
			
			rtobjectNames = parseContext("", root_cxt)
			for rtobjectName in rtobjectNames:
				obj = clientCorbaNaming.resolve(rtobjectName)
				if CORBA.is_nil(obj):
					sys.stdout.write(' - RTObject(%s) not found' % rtobjectName)
					continue
				corbaConsumer = OpenRTM_aist.CorbaConsumer()
				corbaConsumer.setObject(obj)
				try:
					prof = corbaConsumer._ptr().get_component_profile()
					if prof.type_name == 'RobotRTC' and prof.category == 'Simulator':
						robotRTCs[rtobjectName] = corbaConsumer
					elif prof.type_name == 'RangeRTC' and prof.category == 'Simulator':
						rangeRTCs[rtobjectName] = corbaConsumer
					elif prof.type_name == 'CameraRTC' and prof.category == 'Simulator':
						cameraRTCs[rtobjectName] = corbaConsumer
					else:
						if prof.type_name == 'SimulationManager' and prof.category == 'Simulator':

							pass
						else:

							ns, path, port = self.get_host_rtc_paths()
							print clientNS + '/' + rtobjectName
							print ns+'/'+path
							if ns+'/'+path == clientNS+'/'+rtobjectName:
								pass
							else:
								otherRTCs[clientNS+'/'+rtobjectName] = corbaConsumer
				except:
					traceback.print_exc()
					pass

			print robotRTCs
			print otherRTCs
		
			def get_object_profile(rtcs):
				profile_dic = {}
				for n, r in rtcs.items():
					objName = ""
					arg = ""
					try:
						for nv in r._ptr().get_component_profile().properties:
							if nv.name == 'conf.__innerparam.objectName':
								objName = any.from_any(nv.value, keep_structs=True)
							elif nv.name == 'conf.__innerparam.argument':
								arg = any.from_any(nv.value, keep_structs=True)
						profile_dic[objName] = arg
					except:
						pass
				return profile_dic

			self._confRobotsBuffer.set(yaml.dump(get_object_profile(robotRTCs)))
			self._confRangesBuffer.set(yaml.dump(get_object_profile(rangeRTCs)))
			self._confCamerasBuffer.set(yaml.dump(get_object_profile(cameraRTCs)))

			self.rtcMenu['menu'].delete("0", "end")
			for r in otherRTCs.keys():
				self.rtcMenu['menu'].add_command(label=str(r), command= lambda x=str(r): self.synchRTCEntryBuffer.set(x))

			if len(otherRTCs.keys()) > 0:
				self.synchRTCEntryBuffer.set(otherRTCs.keys()[0])
			else:
				self.synchRTCEntryBuffer.set("")
		
		
			if self._simulator._ptr():
				retval, rtcs = self._simulator._ptr().getSynchronizingRTCs()
				if self._fullpath_to_self[0] in rtcs:
					rtcs.remove(self._fullpath_to_self[0])
				ss = yaml.dump(rtcs)
				if len(rtcs) == 1:
					ss = '[' + ss + ']'
				elif len(rtcs) == 0:
					ss = '[]'
				self._confSyncRTCsBuffer.set(ss)
			else:
				self._confSyncRTCsBuffer.set("[]")
			
		except CORBA.TRANSIENT, e:		
			print 'CORBA.TRANSIENT Exception'


	def get_self_rtc_paths(self):
		selfAddr = SELF_RTC_PATH
		clientNS = selfAddr.split('/')[0]
		clientAddr = selfAddr[:selfAddr.rfind(':')][len(clientNS)+1:]
		if clientNS.find(':') < 0: clientNS = clientNS+':2809'
		clientPortName = selfAddr.split(':')[1]
		return clientNS, clientAddr, clientPortName

	def get_host_rtc_paths(self):
		addr = VREP_RTC_PATH
		hostNS = addr.split('/')[0]
		hostAddr   = addr[:addr.rfind(':')][len(hostNS)+1:]
		if hostNS.find(':') < 0: hostNS = hostNS+':2809'
		hostPortName   = addr.split(':')[1]
		return hostNS, hostAddr, hostPortName
		
	def on_connect(self):
		addr = self.connectEntryBuffer.get()
		selfAddr = self.selfEntryBuffer.get()
		
		print ' - Connecting ', selfAddr, ' ServicePort to ', addr 

		clientNS = selfAddr.split('/')[0]
		clientAddr = selfAddr[:selfAddr.rfind(':')][len(clientNS)+1:]
		if clientNS.find(':') < 0: clientNS = clientNS+':2809'
		clientPortName = selfAddr.split(':')[1]
		hostNS = addr.split('/')[0]
		hostAddr   = addr[:addr.rfind(':')][len(hostNS)+1:]
		if hostNS.find(':') < 0: hostNS = hostNS+':2809'
		hostPortName   = addr.split(':')[1]
		
		clientCorbaNaming = OpenRTM_aist.CorbaNaming(OpenRTM_aist.Manager.instance().getORB(), clientNS)

 		clientObj = clientCorbaNaming.resolve(clientAddr)
		if CORBA.is_nil(clientObj):
			sys.stdout.write(' -- Failed to connect %s' % clientAddr)
			return

		client = OpenRTM_aist.CorbaConsumer()
		client.setObject(clientObj)
		clientPorts = client._ptr().get_ports()
		clientPort = None
		for p in clientPorts:
			if p.get_port_profile().name.split('.')[1] == clientPortName:
				clientPort = p

		if not clientPort:
			sys.stdout.write(' -- Failed to find port %s' % clientPort)

		hostCorbaNaming = OpenRTM_aist.CorbaNaming(OpenRTM_aist.Manager.instance().getORB(), clientNS)

		hostObj = hostCorbaNaming.resolve(hostAddr)
		if CORBA.is_nil(hostObj):
			sys.stdout.write(' -- Failed to connect %s' % clientAddr)
			return

		host = OpenRTM_aist.CorbaConsumer()
		host.setObject(hostObj)
		hostPorts = host._ptr().get_ports()
		hostPort = None
		for p in hostPorts:
			if p.get_port_profile().name.split('.')[1] == hostPortName:
				hostPort = p

		if not hostPort:
			sys.stdout.write(' -- Failed to find port %s' % hostPort)
			return

		name = clientPortName + '_to_' + hostPortName
		connector_id = name
		ports = [hostPort, clientPort]
		properties = []
		prof = RTC.ConnectorProfile(name, connector_id, ports, properties)

		ret = hostPort.connect(prof)

		hostECList = host._ptr().get_owned_contexts();
		hostECList[0].activate_component(host._ptr());
		clientECList = client._ptr().get_owned_contexts();
		clientECList[0].activate_component(client._ptr());

		for b in self._enableAfterConnectButton:
			b.config(state=tk.NORMAL)
			pass
		
		
		pass

	def on_save(self):
		import rtctree
		name = self.rtsysNameEntryBuffer.get()
		print 'Saving ', name
		if sys.platform == 'win32':
			p = subprocess.Popen(['rtcryo.bat', self.nsEntryBuffer.get()], stdout=subprocess.PIPE)
		else:
			p = subprocess.Popen(['rtcryo', self.nsEntryBuffer.get()], stdout=subprocess.PIPE)
		p.wait()
		with open(name, "w") as f:
			f.write(p.stdout.read())
			f.close()
			self._sysEntryBuffer.set(name)

	def is_need_gui(self):
		flag = self._simulation_setup_on_activated[0]
		
		return  not (flag=='True' or flag=='true' or flag=='TRUE')
			
		
	def mainloop(self):
		self.root = tk.Tk()
		root = self.root

		"""
		startUpFrame = tk.LabelFrame(root, text="StartUp")
		startUpFrame.grid(padx=5, pady=5, ipadx=5, ipady=5, row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
		startUpLabel = tk.Label(startUpFrame, text="First, connect to simulationRTC.\nTo know the URI of SimulationRTC, RT-SystemEditor is useful.", anchor=tk.NW, justify=tk.LEFT)
		startUpLabel.grid(row=0, column=0, columnspan=3, sticky=tk.W+tk.E, padx=10, pady=5)
		addressLabel = tk.Label(startUpFrame, text="URI of SimulatorRTC")
		addressLabel.grid(row=1, column=0)
		self.connectEntryBuffer = tk.StringVar()
		self.connectEntryBuffer.set("localhost/VREPRTC0.rtc:simulatorPort")
		addressEntry = tk.Entry(startUpFrame, textvariable=self.connectEntryBuffer, width=40)
		addressEntry.grid(row=1, column=1, sticky=tk.W+tk.E)
		connectButton = tk.Button(startUpFrame, text="Connect", command=self.on_connect)
		connectButton.grid(row=1, column=2)
		addressLabel = tk.Label(startUpFrame, text="URI of self (usually no change)")
		addressLabel.grid(row=2, column=0)
		self.selfEntryBuffer = tk.StringVar()
		self.selfEntryBuffer.set("localhost/SimulationManager0.rtc:simulator")
		addressEntry = tk.Entry(startUpFrame, textvariable=self.selfEntryBuffer)
		addressEntry.grid(row=2, column=1, sticky=tk.W+tk.E)
		"""
		setupRTCFrame = tk.LabelFrame(root, text="SetupRTC")
		setupRTCFrame.grid(padx=5, pady=5, row=1, column=0, sticky=tk.N+tk.W+tk.E+tk.S)
		robotLabel = tk.Label(setupRTCFrame, text="Robot Object Name")
		
		_row = 0

		setupRTCLabel = tk.Label(setupRTCFrame, text="Setup RTC in Simulator.\nEnter the object name in Simulator and click Spawn button.\nTo check spawned, use status frame.", justify=tk.LEFT, anchor=tk.NW)
		setupRTCLabel.grid(row=_row, columnspan=4, column=0, sticky=tk.W+tk.E, padx=10, pady=5)

		_row = 1
		robotLabel.grid(row=_row, column=0)
		self.robotEntryBuffer = tk.StringVar()
		self.robotEntryBuffer.set("Robot Object Name")
		robotEntry = tk.Entry(setupRTCFrame, textvariable=self.robotEntryBuffer)
		robotEntry.grid(column=1, row=_row)
		robotArgLabel = tk.Label(setupRTCFrame, text="Argument")
		robotArgLabel.grid(column=2, row=_row)
		self.robotArgEntryBuffer = tk.StringVar()
		self.robotArgEntryBuffer.set("")
		robotArgEntry = tk.Entry(setupRTCFrame, textvariable=self.robotArgEntryBuffer)
		robotArgEntry.grid(column=3, row=_row)
		spawnRobotButton = tk.Button(setupRTCFrame, text="SpawnRobot", command=self.on_spawn_robot)
		spawnRobotButton.grid(column=4, row=_row)

		_row = 2
		rangeLabel = tk.Label(setupRTCFrame, text="Range Object Name")
		rangeLabel.grid(row=_row, column=0)
		self.rangeEntryBuffer = tk.StringVar()
		self.rangeEntryBuffer.set("Range Object Name")
		rangeEntry = tk.Entry(setupRTCFrame, textvariable=self.rangeEntryBuffer)
		rangeEntry.grid(column=1, row=_row)
		rangeArgLabel = tk.Label(setupRTCFrame, text="Argument")
		rangeArgLabel.grid(column=2, row=_row)
		self.rangeArgEntryBuffer = tk.StringVar()
		self.rangeArgEntryBuffer.set("")
		rangeArgEntry = tk.Entry(setupRTCFrame, textvariable=self.rangeArgEntryBuffer)
		rangeArgEntry.grid(column=3, row=_row)
		spawnRangeButton = tk.Button(setupRTCFrame, text="SpawnRange", command=self.on_spawn_range)
		spawnRangeButton.grid(column=4, row=_row)

		_row = 3
		cameraLabel = tk.Label(setupRTCFrame, text="Camera Object Name")
		cameraLabel.grid(row=_row, column=0)
		self.cameraEntryBuffer = tk.StringVar()
		self.cameraEntryBuffer.set("Camera Object Name")
		cameraEntry = tk.Entry(setupRTCFrame, textvariable=self.cameraEntryBuffer)
		cameraEntry.grid(column=1, row=_row)
		cameraArgLabel = tk.Label(setupRTCFrame, text="Argument")
		cameraArgLabel.grid(column=2, row=_row)
		self.cameraArgEntryBuffer = tk.StringVar()
		self.cameraArgEntryBuffer.set("")
		cameraArgEntry = tk.Entry(setupRTCFrame, textvariable=self.cameraArgEntryBuffer)
		cameraArgEntry.grid(column=3, row=_row)
		spawnCameraButton = tk.Button(setupRTCFrame, text="SpawnCamera", command=self.on_spawn_camera)
		spawnCameraButton.grid(column=4, row=_row)

		synchFrame = tk.LabelFrame(root, text="Synchronization")
		synchFrame.grid(padx=5, pady=5, ipadx=5, ipady=5, row=2, columnspan=1, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
		synchLabel = tk.Label(synchFrame, text="Synchronization. If you want to synchronize RTCs outside simulation, \nSelect RTC and Press Synch Button", justify=tk.LEFT, anchor=tk.NW)
		synchLabel.grid(row=0, columnspan=4, column=0, sticky=tk.E+tk.W, padx=10, pady=5)
		f = tk.Frame(synchFrame)
		f.grid(row=1, columnspan=4, column=0, sticky=tk.E+tk.W+tk.N+tk.S)
		rtcLabel = tk.Label(f, text="RTC")
		rtcLabel.grid(row=0, column=0)
		self.synchRTCEntryBuffer =tk.StringVar()
		self.synchRTCEntryBuffer.set("")
		self.rtcMenu = tk.OptionMenu(f, self.synchRTCEntryBuffer, "")
		self.rtcMenu.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
		synchButton = tk.Button(f, text="Synch", command=self.on_synch)
		synchButton.grid(row=0, column=2)
		self.synchronizingRTCList = []

		### RT System Frame
		rtsysFrame = tk.LabelFrame(root, text="RT System")
		rtsysFrame.grid(padx=5, pady=5, ipadx=5, ipady=5, row=3, columnspan=1, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
		rtsysLabel = tk.Label(rtsysFrame, text="RT System Saver. Push save button after constructing RT-System (using RT-System Editor)", justify=tk.LEFT, anchor=tk.NW)
		rtsysLabel.grid(row=0, columnspan=4, column=0, sticky=tk.E+tk.W, padx=10, pady=5)
		nsLabel = tk.Label(rtsysFrame, text="Give Name Server Addresses. Separate with ' '(white space)")
		nsLabel.grid(row=1, column=0)
		self.nsEntryBuffer = tk.StringVar()
		self.nsEntryBuffer.set("localhost:2809")
		nsEntry = tk.Entry(rtsysFrame, textvariable=self.nsEntryBuffer)
		nsEntry.grid(row=1, column=1, stick=tk.E+tk.W)
		rtsysNameLabel = tk.Label(rtsysFrame, text="RT System Profile File Name")
		rtsysNameLabel.grid(row=2, column=0)
		self.rtsysNameEntryBuffer = tk.StringVar()
		self.rtsysNameEntryBuffer.set("rtsystem.xml")
		rtsysNameEntry = tk.Entry(rtsysFrame, textvariable=self.rtsysNameEntryBuffer)
		rtsysNameEntry.grid(row=2, column=1, sticky=tk.E+tk.W)
		rtsysSaveButton = tk.Button(rtsysFrame, text="Save", command=self.on_save)
		rtsysSaveButton.grid(row=2, column=2)

		### Simuation Menus
		simulationFrame = tk.LabelFrame(root, text="Simulation")
		simulationFrame.grid(padx=5, pady=5, ipadx=5, ipady=5, row=4, columnspan=1, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
		simLabel = tk.Label(simulationFrame, text="Setup Simulation Setting. First, Load project file, then you can get all configuration")
		simLabel.grid(row=0, column=0, columnspan=4)
		loadLabel = tk.Label(simulationFrame, text="Simulation Projet File")
		loadLabel.grid(row=1, column=0)
		self.loadEntryBuf = tk.StringVar()
		loadEntry = tk.Entry(simulationFrame, textvariable=self.loadEntryBuf)
		loadEntry.grid(row=1, column=1, sticky=tk.W+tk.E)
		projFindButton = tk.Button(simulationFrame, text="...", command=self.on_proj_find)
		projFindButton.grid(row=1, column=2)
		loadButton = tk.Button(simulationFrame, text="Load", command=self.on_load)
		loadButton.grid(row=1, column=3)
		startButton = tk.Button(simulationFrame, text="Start", command=self.on_start)
		startButton.grid(row=2, column=0)
		stopButton = tk.Button(simulationFrame, text="Stop", command=self.on_stop)
		stopButton.grid(row=3, column=0)

		### Status Informations 
		statusFrame = tk.LabelFrame(root, text="Status")
		statusFrame.grid(padx=5, pady=5, ipadx=5, ipady=5, row=0, rowspan=5, column=1, sticky=tk.N+tk.E+tk.S+tk.W)
		statusLabel = tk.Label(statusFrame, text="Status of Simulation. Click Update button to get info.")
		statusLabel.grid(row=0, column=0, columnspan=2, padx=10, pady=5)
		
		updateLabel = tk.Label(statusFrame, text="Update Information")
		updateLabel.grid(row=1, column=0)
		updateButton = tk.Button(statusFrame, text="Update", command=self.on_update)
		updateButton.grid(row=1, column=2)
		robotsLabel = tk.Label(statusFrame, text="conf.default.robots")
		robotsLabel.grid(row=2, column=0)
		self._confRobotsBuffer = tk.StringVar()
		self._confRobotsBuffer.set("{}")
		robotsEntry = tk.Entry(statusFrame, textvariable=self._confRobotsBuffer)
		robotsEntry.grid(row=2, column=1, columnspan=2)
		rangesLabel = tk.Label(statusFrame, text="conf.default.ranges")
		rangesLabel.grid(row=3, column=0)
		self._confRangesBuffer = tk.StringVar()
		self._confRangesBuffer.set("{}")
		rangesEntry = tk.Entry(statusFrame, textvariable=self._confRangesBuffer)
		rangesEntry.grid(row=3, column=1, columnspan=2)
		camerasLabel = tk.Label(statusFrame, text="conf.default.cameras")
		camerasLabel.grid(row=4, column=0)
		self._confCamerasBuffer = tk.StringVar()
		self._confCamerasBuffer.set("{}")
		camerasEntry = tk.Entry(statusFrame, textvariable=self._confCamerasBuffer)
		camerasEntry.grid(row=4, column=1, columnspan=2)
		syncLabel = tk.Label(statusFrame, text="conf.default.sync_rtcs")
		syncLabel.grid(row=5, column=0)
		self._confSyncRTCsBuffer = tk.StringVar()
		self._confSyncRTCsBuffer.set("[]")
		sync_rtcsEntry = tk.Entry(statusFrame, textvariable=self._confSyncRTCsBuffer)
		sync_rtcsEntry.grid(row=5, column=1, columnspan=2)
		sysLabel = tk.Label(statusFrame, text="conf.default.rtsystem")
		sysLabel.grid(row=6, column=0)
		self._sysEntryBuffer = tk.StringVar()
		self._sysEntryBuffer.set("None")
		sysEntry = tk.Entry(statusFrame, textvariable=self._sysEntryBuffer)
		sysEntry.grid(row=6, column=1, columnspan=2)

		projLabel = tk.Label(statusFrame, text="conf.default.project")
		projLabel.grid(row=7, column=0)
		self._projEntryBuffer = tk.StringVar()
		self._projEntryBuffer.set("None")
		projEntry = tk.Entry(statusFrame, textvariable=self._projEntryBuffer)
		projEntry.grid(row=7, column=1, columnspan=2)

		simTimesLabel = tk.Label(statusFrame, text="conf.default.simulation_times")
		simTimesLabel.grid(row=8, column=0)
		self._simTimesEntryBuffer = tk.StringVar()
		self._simTimesEntryBuffer.set("0")
		simTimesEntry = tk.Entry(statusFrame, textvariable=self._simTimesEntryBuffer)
		simTimesEntry.grid(row=8, column=1, columnspan=2)

		simEndConditionLabel = tk.Label(statusFrame, text="conf.default.simulation_end_condition")
		simEndConditionLabel.grid(row=9, column=0)
		self._simEndConditionEntryBuffer = tk.StringVar()
		self._simEndConditionEntryBuffer.set("timespan")
		simEndConditionEntry = tk.OptionMenu(statusFrame, self._simEndConditionEntryBuffer, "timespan", "rtcactivated", "rtcdeactivated", "rtcerror")
		simEndConditionEntry.grid(row=9, column=1, columnspan=2)

		simEndTimespanLabel = tk.Label(statusFrame, text="conf.default.simulation_end_timespan")
		simEndTimespanLabel.grid(row=10, column=0)
		self._simEndTimespanEntryBuffer = tk.StringVar()
		self._simEndTimespanEntryBuffer.set("10.0")
		simEndTimespanEntry = tk.Entry(statusFrame, textvariable=self._simEndTimespanEntryBuffer)
		simEndTimespanEntry.grid(row=10, column=1, columnspan=2)

		simEndRTCPathLabel = tk.Label(statusFrame, text="conf.default.simulation_end_rtcpath")
		simEndRTCPathLabel.grid(row=11, column=0)
		self._simEndRTCPathEntryBuffer = tk.StringVar()
		self._simEndRTCPathEntryBuffer.set("localhost:2809/VREPRTC0.rtc")
		simEndRTCPathEntry = tk.Entry(statusFrame, textvariable=self._simEndRTCPathEntryBuffer)
		simEndRTCPathEntry.grid(row=11, column=1, columnspan=2)

		saveLabel = tk.Label(statusFrame, text="Save Configuration to SimulationManager.conf")
		saveLabel.grid(row=12, column=0, columnspan=2)
		saveButton = tk.Button(statusFrame, text="Save", command=self.on_save_conf)
		saveButton.grid(row=12, column=2, columnspan=1)


		self._enableAfterConnectButton = [
			spawnRobotButton, spawnRangeButton, spawnCameraButton, synchButton,
			loadButton]

		#for b in self._enableAfterConnectButton:
		#	b.config(state=tk.DISABLED)

		#root.after(3000, self.on_after)
		root.mainloop()

	def on_after(self):
		self.on_update()
		self.root.after(3000, self.on_after)



def SimulationManagerInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=simulatortest_spec)
    manager.registerFactory(profile,
                            SimulationManager,
                            OpenRTM_aist.Delete)

comp = None

def MyModuleInit(manager):
    SimulationManagerInit(manager)

    # Create a component
    global comp
    comp = manager.createComponent("SimulationManager?naming.formats=%n.rtc")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	global comp
	if comp.is_need_gui():
		print 'GUI'
		mgr.runManager(True)
		comp.mainloop()
		mgr.shutdown()
	else:
		print 'NO GUI'
		mgr.runManager(False)

if __name__ == "__main__":
	main()

