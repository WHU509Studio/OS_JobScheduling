"""磁盘调度算法实现
先来先服务算法：按照请求磁盘的先后顺序进行调度
最短寻道时间优先：选择当前磁头所在的磁道距离最近的请求作为下一次服务的对象
扫描算法(电梯调度算法)：从一端开始往复移动
循环扫描算法：扫描算法+单项移动
"""

from typing import List, Union
from dataclasses import dataclass
from copy import deepcopy


@dataclass
class RequestInfo:
    order: int
    track: int
    visited: bool = False


def wrap_data(
        *,
        request_orders: List[int] = None,
        request_tracks: List[int]
) -> List[RequestInfo]:
    if request_orders:
        assert len(request_orders) == len(request_tracks)
    else:
        request_orders = [i for i in range(1, len(request_tracks)+1)]

    return [RequestInfo(*info) for info in zip(request_orders, request_tracks)]


def first_come_first_serve(current_track: int, wrapped_data: List[RequestInfo]) -> None:
    sorted_wrapped_data = sorted(wrapped_data, key=lambda x: x.order)

    total_cost = 0
    order_list = []

    for data in sorted_wrapped_data:
        total_cost += abs(data.track - current_track)
        current_track = data.track
        order_list.append(f"{data.order}")

    print(f"请求次序为：{'->'.join(order_list)}")
    print(f"总共经过的柱面数：{total_cost}")


def shortest_seek_time_first(current_track: int, wrapped_data: List[RequestInfo]) -> None:
    def find_shortest_index(track: int, data: List[RequestInfo]) -> int:
        index = -1
        shortest = float("inf")

        for i, request in enumerate(data):
            if request.visited:
                continue
            else:
                cost = abs(track - request.track)
                if shortest > abs(track - request.track):
                    shortest = cost
                    index = i
        return index

    wrapped_data_copy = deepcopy(wrapped_data)

    total_cost = 0
    order_list = []

    for _ in range(len(wrapped_data_copy)):
        next_index = find_shortest_index(current_track, wrapped_data_copy)
        wrapped_data_copy[next_index].visited = True
        total_cost += abs(current_track-wrapped_data_copy[next_index].track)
        order_list.append(f"{wrapped_data_copy[next_index].order}")
        current_track = wrapped_data_copy[next_index].track

    print(f"请求次序为：{'->'.join(order_list)}")
    print(f"总共经过的柱面数：{total_cost}")


def scan(big: bool, current_track: int, wrapped_data: List[RequestInfo], mode="scan") -> None:
    def find_current_index(track: int, data: List[RequestInfo]):
        for i, request in enumerate(data):
            if request.visited:
                continue
            if request.track >= track:
                return i
        return len(data)
    def find_next_index(big: bool, track: int, data: List[RequestInfo]):
        idx = find_current_index(track, data)
        if big:
            for i in range(idx, len(data)):
                request = data[i]
                if request.visited:
                    continue
                return i
        else:
            for i in range(idx-1, -1, -1):
                request = data[i]
                if request.visited:
                    continue
                return i

        # 失败，返回-1
        return -1

    # big 是否向磁道变大的方向移动
    sorted_wrapped_data = sorted(deepcopy(wrapped_data), key=lambda x: x.track)

    total_cost = 0
    order_list = []

    for _ in range(len(sorted_wrapped_data)):
        idx = find_next_index(big, current_track, sorted_wrapped_data)
        if idx == -1:
            if mode == "scan":
                big = not big
                idx = find_next_index(big, current_track, sorted_wrapped_data)
            elif mode == "cscan":
                if big:
                    total_cost += abs(current_track-sorted_wrapped_data[0].track)
                    current_track = sorted_wrapped_data[0].track
                else:
                    total_cost += abs(current_track-sorted_wrapped_data[-1].track)
                    current_track = sorted_wrapped_data[-1].track
                idx = find_next_index(big, current_track, sorted_wrapped_data)

        request = sorted_wrapped_data[idx]
        request.visited = True
        total_cost += abs(current_track - request.track)
        order_list.append(f"{request.order}")
        current_track = request.track

    print(f"请求次序为：{'->'.join(order_list)}")
    print(f"总共经过的柱面数：{total_cost}")


if __name__ == '__main__':
    test1 = wrap_data(
        request_orders=[1, 2, 3, 4, 5, 6, 7, 8],
        request_tracks=[88, 2, 60, 94, 45, 29, 16, 56]
    )
    test2 = wrap_data(
        request_orders=[1, 2, 3, 4, 5, 6, 7, 8, 9],
        request_tracks=[90, 58, 55, 39, 38, 18, 150, 160, 184]
    )

    # first_come_first_serve(20, test1)
    shortest_seek_time_first(20, test1)
    shortest_seek_time_first(100, test2)

    scan(True, 100, test2)
    scan(True, 100, test2, mode="cscan")
    scan(True, 20, test1, mode="cscan")