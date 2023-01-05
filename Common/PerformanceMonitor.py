import time

class PerformanceMonitor():
    def __init__(self, jobName, recordsPerUpdate, totalRecordCount = None) -> None:
        self.jobName = jobName
        self.recordsPerUpdate = recordsPerUpdate
        self.totalRecordCount = totalRecordCount
        self.position = 0
        self.startTime = time.time()

    
    def tick(self, actionsPerformed = 1):
        self.position += actionsPerformed

        if self.position % self.recordsPerUpdate != 0:
            return

        currentTime = time.time()
        elapsedTime = currentTime - self.startTime

        processingEndPoint = self.position + self.recordsPerUpdate

        recordsPerHour = self.position / (elapsedTime / 60 / 60)
        formattedRecordsPerHour = "{:,.2f}".format(recordsPerHour)

        if self.totalRecordCount != None and processingEndPoint > self.totalRecordCount:
            processingEndPoint = self.totalRecordCount

        print((f"{self.jobName} - processing records {self.position:,} - {processingEndPoint:,}"
            f" at {formattedRecordsPerHour} records per hour"))
