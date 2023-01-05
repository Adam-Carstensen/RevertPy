from Common.PerformanceMonitor import PerformanceMonitor
import time

maxRange = 10000

performanceMonitor = PerformanceMonitor("Performance Monitor Example", recordsPerUpdate=1000, totalRecordCount=maxRange)

for index in range(maxRange):
    performanceMonitor.tick()
    time.sleep(0.001)
