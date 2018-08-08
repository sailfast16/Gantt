import requests
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GanttChart.settings")

from Lanes.models import Task

class Lane:
    def __init__(self, name, length):
        self.id = name
        self.length = length
        self.jobs = {}
        self.free_spaces = [(0, self.length)]
        self.remaining = self.length

    def findFit(self, win_start, win_end, job_len):
        fits = []
        space = (0, 0)
        for s in self.free_spaces:
            not_done = True

            # Check if free space is big enough to fit the task
            if s[1] - s[0] < job_len:
                continue

            else:
                if s[0] < win_start:
                    position = (win_start, win_start+job_len)

                else:
                    position = (s[0], s[0]+job_len)

            # check if task is completed outside of time window
            if position[1] > win_end:
                continue

            # check if Task is compleated outside of the free space
            if position[1] > s[1]:
                continue

            # check if the task has slid past the free space
            if position[0] >= s[1]:
                continue

            while not_done:
                if s[0] <= position[0] and position[1] <= s[1]:
                    not_done = False
                    fits.append(position)
                    space = s

                else:
                    position += (1, 1)

        if len(fits) == 0:
            return -1

        else:
            return fits[0], space

    # splits the empty space in the lane into seperate pieces
    def splitLane(self, _start, _end, space):
        if space[0] != _start:
            self.free_spaces.append((space[0], _start))

        if space[1] != _end:
            self.free_spaces.append((_end, space[1]))

        self.free_spaces.remove(space)


    def add_job(self, job):
        try:
            (_space, _old) = self.findFit(job['least_start'], job['max_end'], job['length'])
            _start = _space[0]
            _end = _start + job['length']
            self.jobs[job['id']] = (_start, _end)
            self.splitLane(_start, _end, _old)
        except TypeError:
            return -1

        self.remaining -= job['length']

    def __eq__(self, other):
        return self.remaining == other.remaining

    def __lt__(self, other):
        return self.remaining < other.remaining

    def __gt__(self, other):
        return self.remaining > other.remaining

    def __str__(self):
        return '(jobs=%s, remaining=%s)' % (str(self.jobs), self.remaining)


class laneList(object):
    def __init__(self, lane_size):
        self.lane_size = lane_size
        self.lanes = []
        self.numLanes = 0
        self.extra = 0

    def add_lane(self):
        self.lanes.append(Lane(self.numLanes + 1, self.lane_size))
        self.numLanes = len(self.lanes)
        self.lanes = sorted(self.lanes)

    def get_extra(self):
        self.extra = 0
        for i in range(self.numLanes):
            self.extra += self.lanes[i].remaining

    def FF(self, job):
        current = 0
        not_done = True
        while not_done:
            if len(self.lanes) == 0:
                self.add_lane()

            try:
                if self.lanes[current].add_job(job) != -1:
                    not_done = False
                    self.get_extra()
                    break

                else:
                    current += 1

            except IndexError:
                self.add_lane()


    def __str__(self):
        if self.numLanes != 0:
            for lane in self.lanes:
                print(lane)
            return 'Number of Lanes: %s, Free Space: %s' % (self.numLanes, self.extra)
        else:
            return 'No Lanes'


def run():
    json_url = 'http://127.0.0.1:8000/tasksJSON/'
    f = requests.get(json_url)
    json_data = f.json()

    jobs = []
    fixed_jobs = []
    for task in json_data:
        if task['fixed']:
            fixed_jobs.append(task)
        else:
            jobs.append(task)

    # TODO: this can't actually be a fixed lane length
    lanes = laneList(500)
    for job in fixed_jobs:
        lanes.FF(job)
    for job in jobs:
        lanes.FF(job)

    lane_list = {}
    for lane in lanes.lanes:
        lane_list[lane.id] = lane.jobs

    for key, values in lane_list.items():
        for k, v in lane_list[key].items():
            task = Task.objects.get(pk=k)
            task.resources = key
            task.start = v[0]
            task.end = v[1]
            task.save()




