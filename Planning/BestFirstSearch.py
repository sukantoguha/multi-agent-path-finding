from heapq import heappush, heappop
from Planning.ClosedList import ClosedList

class BestFirstSearch:

    @staticmethod
    def plan(start_state):
        open = []
        closed = ClosedList()
        heappush(open, start_state)
        closed.insert(start_state)
        while open:
            u = heappop(open)
            #print("u : ", u)
            if u.is_goal():
                ans = []
                u.get_plan(ans)
                # return plan
                return ans
            else:

                successors = u.expand()
                #print("successors : ", successors)
                for v in successors:
                    #print("v : ", v)
                    #print(" successor element : ", v)
                    #  if v is in closed
                    if v in closed:
                        # if v.f >= closed(v).f
                        if v >= closed.get(v):
                            # continue
                            continue
                        else:
                            closed.remove(v)
                    # insert v to open and closed
                    heappush(open, v)
                    closed.insert(v)
        raise ValueError('No valid path exist from %s' % start_state)