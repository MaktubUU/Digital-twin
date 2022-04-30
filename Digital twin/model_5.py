'''
Date: 2022-04-19 15:33:19
LastEditors: ZSudoku
LastEditTime: 2022-04-30 14:58:37
FilePath: \Digital-twin\Digital twin\model_5.py
立库模块，主要计算堆垛机的任务
'''
import mysql_goodsLocationInfo as CargoNow_sql
import mysql_productionLineData as ddjData_sql
import copy

CargoNow = [{'x': 1869.90466, 'y': 19.9703217, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 3, 'column': 26, 'type': '10', 'id': 'A-7-3-26', 'bidBatch': '', 'factory': '', 'num': 1}, {'x': 1869.26843, 'y': 7.68457127, 'z': 53.2860031, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 2, 'column': 10, 'type': '10', 'id': 'B-16-2-10', 'bidBatch': '', 'factory': '', 'num': 2}, {'x': 1878.222, 'y': 18.434639, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 16, 'column': 24, 'type': '10', 'id': 'B-8-16-24', 'bidBatch': '', 'factory': '', 'num': 3}, {'x': 1881.42786, 'y': 18.434639, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 21, 'column': 24, 'type': '10', 'id': 'A-15-21-24', 'bidBatch': '', 'factory': '', 'num': 4}, {'x': 1900.63, 'y': 19.2024612, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 51, 'column': 25, 'type': '10', 'id': 'A-9-51-25', 'bidBatch': '', 'factory': '', 'num': 5}, {'x': 1889.743, 'y': 16.1310234, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 34, 'column': 21, 'type': '10', 'id': 'A-7-34-21', 'bidBatch': '', 'factory': '', 'num': 6}, {'x': 1898.0625, 'y': 15.3631821, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 47, 'column': 20, 'type': '10', 'id': 'A-15-47-20', 'bidBatch': '', 'factory': '', 'num': 7}, {'x': 1871.82764, 'y': 19.9703979, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 6, 'column': 26, 'type': '10', 'id': 'B-8-6-26', 'bidBatch': '', 'factory': '', 'num': 8}, {'x': 1889.10876, 'y': 1.54167175, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 33, 'column': 2, 'type': '11', 'id': 'B-10-33-2', 'bidBatch': '', 'factory': '', 'num': 9}, {'x': 1868.62036, 'y': 15.3631821, 'z': 53.2860031, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 1, 'column': 20, 'type': '11', 'id': 'B-16-1-20', 'bidBatch': '', 'factory': '', 'num': 10}, {'x': 1878.222, 'y': 19.2024612, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 16, 'column': 25, 'type': '11', 'id': 'A-9-16-25', 'bidBatch': '', 'factory': '', 'num': 11}, {'x': 1890.38525, 'y': 18.434639, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 35, 'column': 24, 'type': '11', 'id': 'B-6-35-24', 'bidBatch': '', 'factory': '', 'num': 12}, {'x': 1892.94763, 'y': 17.6667786, 'z': 53.286, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 39, 'column': 23, 'type': '11', 'id': 'B-16-39-23', 'bidBatch': '', 'factory': '', 'num': 13}, {'x': 1879.50464, 'y': 16.8989182, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 18, 'column': 22, 'type': '11', 'id': 'A-15-18-22', 'bidBatch': '', 'factory': '', 'num': 14}, {'x': 1871.18518, 'y': 6.14884233, 'z': 53.2860031, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 5, 'column': 8, 'type': '13', 'id': 'B-16-5-8', 'bidBatch': '', 'factory': '', 'num': 15}, {'x': 1868.62036, 'y': 8.452438, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 1, 'column': 11, 'type': '13', 'id': 'A-15-1-11', 'bidBatch': '', 'factory': '', 'num': 16}, {'x': 1892.31165, 'y': 10.7560148, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 38, 'column': 14, 'type': '13', 'id': 'A-15-38-14', 'bidBatch': '', 'factory': '', 'num': 17}, {'x': 1874.38452, 'y': 16.1310234, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 10, 'column': 21, 'type': '13', 'id': 'A-13-10-21', 'bidBatch': '', 'factory': '', 'num': 18}, {'x': 1898.70679, 'y': 13.8274679, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 48, 'column': 18, 'type': '13', 'id': 'A-13-48-18', 'bidBatch': '', 'factory': '', 'num': 19}, {'x': 1898.70679, 'y': 11.5238724, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 48, 'column': 15, 'type': '13', 'id': 'A-15-48-15', 'bidBatch': '', 'factory': '', 'num': 20}, {'x': 1882.06409, 'y': 19.9703217, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 22, 'column': 26, 'type': '15', 'id': 'A-9-22-26', 'bidBatch': '', 'factory': '', 'num': 21}, {'x': 1875.02258, 'y': 7.68457127, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 11, 'column': 10, 'type': '15', 'id': 'A-15-11-10', 'bidBatch': '', 'factory': '', 'num': 22}, {'x': 1898.06311, 'y': 18.434639, 'z': 53.286, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 47, 'column': 24, 'type': '15', 'id': 'B-16-47-24', 'bidBatch': '', 'factory': '', 'num': 23}, {'x': 1874.38452, 'y': 16.1310234, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 10, 'column': 21, 'type': '15', 'id': 'A-11-10-21', 'bidBatch': '', 'factory': '', 'num': 24}, {'x': 1870.54688, 'y': 15.3631821, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 4, 'column': 20, 'type': '15', 'id': 'A-15-4-20', 'bidBatch': '', 'factory': '', 'num': 25}, {'x': 1869.26843, 'y': 17.6667786, 'z': 53.286, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 2, 'column': 23, 'type': '15', 'id': 'B-16-2-23', 'bidBatch': '', 'factory': '', 'num': 26}, {'x': 1891.02551, 'y': 13.8274679, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 36, 'column': 18, 'type': '15', 'id': 'A-15-36-18', 'bidBatch': '', 'factory': '', 'num': 27}, {'x': 1884.62317, 'y': 16.1310234, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 26, 'column': 21, 'type': '16', 'id': 'B-8-26-21', 'bidBatch': '', 'factory': '', 'num': 28}, {'x': 1871.18518, 'y': 18.434639, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 5, 'column': 24, 'type': '16', 'id': 'B-6-5-24', 'bidBatch': '', 'factory': '', 'num': 29}, {'x': 1892.31165, 'y': 13.0595894, 'z': 50.35678, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 38, 'column': 17, 'type': '16', 'id': 'B-14-38-17', 'bidBatch': '', 'factory': '', 'num': 30}, {'x': 1882.71045, 'y': 16.1310616, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 23, 'column': 21, 'type': '16', 'id': 'B-6-23-21', 'bidBatch': '', 'factory': '', 'num': 31}, {'x': 1898.0625, 'y': 18.434639, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 47, 'column': 24, 'type': '16', 'id': 'A-13-47-24', 'bidBatch': '', 'factory': '', 'num': 32}, {'x': 1877.58569, 'y': 10.7560148, 'z': 53.2860031, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 15, 'column': 14, 'type': '16', 'id': 'B-16-15-14', 'bidBatch': '', 'factory': '', 'num': 33}, {'x': 1888.46655, 'y': 19.2025337, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 32, 'column': 25, 'type': '16', 'id': 'B-8-32-25', 'bidBatch': '', 'factory': '', 'num': 34}, {'x': 1892.94763, 'y': 13.0595894, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 39, 'column': 17, 'type': '16', 'id': 'B-12-39-17', 'bidBatch': '', 'factory': '', 'num': 35}, {'x': 1882.71045, 'y': 13.0595894, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 23, 'column': 17, 'type': '16', 'id': 'A-13-23-17', 'bidBatch': '', 'factory': '', 'num': 36}, {'x': 1883.3446, 'y': 19.2024975, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 24, 'column': 25, 'type': '16', 'id': 'A-5-24-25', 'bidBatch': '', 'factory': '', 'num': 37}, {'x': 1896.14722, 'y': 8.452438, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 44, 'column': 11, 'type': '16', 'id': 'A-15-44-11', 'bidBatch': '', 'factory': '', 'num': 38}, {'x': 1898.70679, 'y': 19.97036, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 48, 'column': 26, 'type': '16', 'id': 'A-5-48-26', 'bidBatch': '', 'factory': '', 'num': 39}, {'x': 1886.54578, 'y': 17.6667786, 'z': 48.6279373, 's1': 1, 's2': 0, 'flag': 'A', 'line': 13, 'row': 23, 'column': 29, 'type': 10, 'id': 'A-13-29-23', 'bidBatch': '2019年第一批', 'factory': '杭州炬华', 'num': 40}, {'x': 1883.98486, 'y': 8.452438, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 11, 'column': 25, 'type': 10, 'id': 'A-9-25-11', 'bidBatch': '2019年第二批', 'factory': '杭州炬华', 'num': 41}, {'x': 1872.464, 'y': 5.380984, 'z': 42.17527, 's1': 1, 's2': 0, 'flag': 'B', 'line': 8, 'row': 7, 'column': 7, 'type': 10, 'id': 'B-8-7-7', 'bidBatch': '2020年第一批', 'factory': '宁夏隆基', 'num': 42}, {'x': 1871.82764, 'y': 3.84524536, 'z': 42.17527, 's1': 1, 's2': 0, 'flag': 'B', 'line': 8, 'row': 5, 'column': 6, 'type': 10, 'id': 'B-8-6-5', 'bidBatch': '2021年第一批', 'factory': '杭州炬华', 'num': 43}, {'x': 1883.98486, 'y': 17.6667786, 'z': 47.6289978, 's1': 1, 's2': 0, 'flag': 'B', 'line': 12, 'row': 23, 'column': 25, 'type': 10, 'id': 'B-12-25-23', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 44}, {'x': 1876.30713, 'y': 6.14884233, 'z': 38.3443832, 's1': 1, 's2': 0, 'flag': 'B', 'line': 6, 'row': 8, 'column': 13, 'type': 10, 'id': 'B-6-13-8', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 45}, {'x': 1889.10876, 'y': 15.3631821, 'z': 45.8976822, 's1': 1, 's2': 0, 'flag': 'A', 'line': 11, 'row': 20, 'column': 33, 'type': 10, 'id': 'A-11-33-20', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 46}, {'x': 1871.18518, 'y': 15.3632011, 'z': 38.3443832, 's1': 1, 's2': 0, 'flag': 'B', 'line': 6, 'row': 20, 'column': 5, 'type': 10, 'id': 'B-6-5-20', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 47}, {'x': 1870.54688, 'y': 13.8274679, 'z': 48.6279373, 's1': 1, 's2': 0, 'flag': 'A', 'line': 13, 'row': 18, 'column': 4, 'type': 15, 'id': 'A-13-4-18', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 48}, {'x': 1899.98157, 'y': 19.2024975, 'z': 50.3567772, 's1': 1, 's2': 0, 'flag': 'B', 'line': 14, 'row': 25, 'column': 50, 'type': 15, 'id': 'B-14-50-25', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 49}, {'x': 1877.58582, 'y': 0.7738123, 'z': 36.62432, 's1': 1, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 15, 'type': 15, 'id': 'A-5-15-1', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 50}, {'x': 1893.59387, 'y': 4.613105, 'z': 42.17527, 's1': 1, 's2': 0, 'flag': 'B', 'line': 8, 'row': 6, 'column': 40, 'type': 15, 'id': 'B-8-40-6', 'bidBatch': '2020年第一批', 'factory': '深圳科陆', 'num': 51}, {'x': 1885.90771, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 0, 'flag': 'A', 'line': 13, 'row': 3, 'column': 28, 'type': 15, 'id': 'A-13-28-3', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 52}, {'x': 1883.3446, 'y': 4.613105, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 6, 'column': 24, 'type': 15, 'id': 'A-9-24-6', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 53}, {'x': 1886.54578, 'y': 17.6667786, 'z': 48.6279373, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 23, 'column': 29, 'type': 10, 'id': 'A-13-29-23', 'bidBatch': '2019年第一批', 'factory': '杭州炬华', 'num': 54}, {'x': 1883.98486, 'y': 8.452438, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 11, 'column': 25, 'type': 10, 'id': 'A-9-25-11', 'bidBatch': '2019年第二批', 'factory': '杭州炬华', 'num': 55}, {'x': 1872.464, 'y': 5.380984, 'z': 42.17527, 's1': 0, 's2': 1, 'flag': 'B', 'line': 8, 'row': 7, 'column': 7, 'type': 10, 'id': 'B-8-7-7', 'bidBatch': '2020年第一批', 'factory': '宁夏隆基', 'num': 56}, {'x': 1871.82764, 'y': 3.84524536, 'z': 42.17527, 's1': 0, 's2': 1, 'flag': 'B', 'line': 8, 'row': 5, 'column': 6, 'type': 10, 'id': 'B-8-6-5', 'bidBatch': '2021年第一批', 'factory': '杭州炬华', 'num': 57}, {'x': 1883.98486, 'y': 17.6667786, 'z': 47.6289978, 's1': 0, 's2': 1, 'flag': 'B', 'line': 12, 'row': 23, 'column': 25, 'type': 10, 'id': 'B-12-25-23', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 58}, {'x': 1876.30713, 'y': 6.14884233, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 8, 'column': 13, 'type': 10, 'id': 'B-6-13-8', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 59}, {'x': 1889.10876, 'y': 15.3631821, 'z': 45.8976822, 's1': 0, 's2': 1, 'flag': 'A', 'line': 11, 'row': 20, 'column': 33, 'type': 10, 'id': 'A-11-33-20', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 60}, {'x': 1871.18518, 'y': 15.3632011, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 20, 'column': 5, 'type': 10, 'id': 'B-6-5-20', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 61}, {'x': 1870.54688, 'y': 13.8274679, 'z': 48.6279373, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 18, 'column': 4, 'type': 15, 'id': 'A-13-4-18', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 62}, {'x': 1899.98157, 'y': 19.2024975, 'z': 50.3567772, 's1': 0, 's2': 1, 'flag': 'B', 'line': 14, 'row': 25, 'column': 50, 'type': 15, 'id': 'B-14-50-25', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 63}, {'x': 1877.58582, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 1, 'flag': 'A', 'line': 5, 'row': 1, 'column': 15, 'type': 15, 'id': 'A-5-15-1', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 64}, {'x': 1893.59387, 'y': 4.613105, 'z': 42.17527, 's1': 0, 's2': 1, 'flag': 'B', 'line': 8, 'row': 6, 'column': 40, 'type': 15, 'id': 'B-8-40-6', 'bidBatch': '2020年第一批', 'factory': '深圳科陆', 'num': 65}, {'x': 1885.90771, 'y': 2.3095293, 'z': 48.62794, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 28, 'type': 15, 'id': 'A-13-28-3', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 66}, {'x': 1883.3446, 'y': 4.613105, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 6, 'column': 24, 'type': 15, 'id': 'A-9-24-6', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 67}, {'x': 1871.82764, 'y': 6.14884233, 'z': 38.3443832, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 8, 'column': 6, 'type': 10, 'id': 'B-6-6-8', 'bidBatch': '2021年第一批', 'factory': '宁夏隆基', 'num': 68}, {'x': 1873.74841, 'y': 10.7560148, 'z': 42.17527, 's1': 1, 's2': 1, 'flag': 'B', 'line': 8, 'row': 14, 'column': 9, 'type': 10, 'id': 'B-8-9-14', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 69}, {'x': 1887.82837, 'y': 7.68457127, 'z': 50.35678, 's1': 1, 's2': 1, 'flag': 'B', 'line': 14, 'row': 10, 'column': 31, 'type': 10, 'id': 'B-14-31-10', 'bidBatch': '2019年第二批', 'factory': '深圳科陆', 'num': 70}, {'x': 1888.46655, 'y': 13.8274679, 'z': 42.17527, 's1': 1, 's2': 1, 'flag': 'B', 'line': 8, 'row': 18, 'column': 32, 'type': 11, 'id': 'B-8-32-18', 'bidBatch': '2020年第一批', 'factory': '深圳科陆', 'num': 71}, {'x': 1889.743, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 34, 'type': 11, 'id': 'A-13-34-3', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 72}, {'x': 1896.7876, 'y': 6.916702, 'z': 50.35678, 's1': 1, 's2': 1, 'flag': 'B', 'line': 14, 'row': 9, 'column': 45, 'type': 11, 'id': 'B-14-45-9', 'bidBatch': '2016年第一批', 'factory': '深圳科陆', 'num': 73}, {'x': 1899.34912, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 49, 'type': 11, 'id': 'A-13-49-3', 'bidBatch': '2019年第二批', 'factory': '杭州炬华', 'num': 74}, {'x': 1874.38452, 'y': 9.220296, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 12, 'column': 10, 'type': 11, 'id': 'A-9-10-12', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 75}, {'x': 1875.66882, 'y': 16.1310234, 'z': 47.6289978, 's1': 1, 's2': 1, 'flag': 'B', 'line': 12, 'row': 21, 'column': 12, 'type': 11, 'id': 'B-12-12-21', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 76}, {'x': 1896.7876, 'y': 1.54167175, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 2, 'column': 45, 'type': 13, 'id': 'A-5-45-2', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 77}, {'x': 1871.82764, 'y': 1.5416708, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 2, 'column': 6, 'type': 13, 'id': 'A-9-6-2', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 78}, {'x': 1900.63, 'y': 1.54167175, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 2, 'column': 51, 'type': 13, 'id': 'A-13-51-2', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 79}, {'x': 1901.27039, 'y': 1.54167175, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 2, 'column': 52, 'type': 13, 'id': 'A-11-52-2', 'bidBatch': '2021年第一批', 'factory': '苏源杰瑞', 'num': 80}, {'x': 1873.74841, 'y': 0.7738123, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 1, 'column': 9, 'type': 13, 'id': 'A-5-9-1', 'bidBatch': '2019年第一批', 'factory': '深圳科陆', 'num': 81}, {'x': 1880.14307, 'y': 4.613105, 'z': 53.2860031, 's1': 1, 's2': 1, 'flag': 'B', 'line': 16, 'row': 6, 'column': 19, 'type': 15, 'id': 'B-16-19-6', 'bidBatch': '2021年第一批', 'factory': '宁波三星', 'num': 82}, {'x': 1882.71045, 'y': 4.613105, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 6, 'column': 23, 'type': 15, 'id': 'A-11-23-6', 'bidBatch': '2020年第一批', 'factory': '苏源杰瑞', 'num': 83}, {'x': 1877.58582, 'y': 11.5238724, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 15, 'column': 15, 'type': 15, 'id': 'A-5-15-15', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 84}]
#CargoNow = CargoNow_sql.getGoodsLocationInfoVice()
R = 39
S = 14
H = 14
C = 17
LineTimeList=[ 31.84, 32.69, 34.55, 35.41, 37.29, 38.15, 40.02, 40.88, 42.78, 44.70, 46.58 ]
LisCross = [[[1,3,47.11],[3,4,17.78]],[[2,3,5.17],[3,4,17.78]]] #程天宇计算
#各种类型的上货数量  
LisGoodsNum = [{'10':8,'11':6,'13':6,'15':7,'16':12}]
dirInspect = {'10':8,'15':6}
#3箱一垛或者是5箱一垛
mod1 = 3
mod2 = 5
inrTime = 4 #叠一次货物运行时长
flodTime = 5 #两次叠箱间的等待时长
lostTime = inrTime + flodTime 


graph_of_spots = [  #陈薛强输出
    [1, 10, 9, 2.5],
    [1, 11, 9, 2.1],
    [2, 9, 5, 2.3],
    [3, 4, 2, 2.4],
    [3, 5, 2, 1.5],
    [3, 6, 2, 1.4],
    [4, 2, 1, 2.5],
    [6, 1, 3, 3],
    [7, 3, 8, 3.4],
    [7, 3, 7, 3.1]
]

fold_id = 1  # 叠箱机的 id  陈薛强输出
global LisDdjTime 
global LisDdjTimeD
global LisInspect
global LisReturnTime
global inspectIndex #已读送检数量
global returnIndex  #已读回库数量
global LisEnterTime #入库资产到达对应入库口的时间
global DdjEnterXYZ
global DdjOutXYZ
global DdjInspectXYZ
global InspectTypeFloorNum
global ReadInspectTypeNum
global DirReturnXYZ
global rrr#每个堆垛机对应的line，二维list
global ans#所有line编号,一维set
global r#所有入库的编号,一维set
global dr#每个入库编号对应的line编号,一维dict3
global lineToDdj
global idToL

lineToDdj={};
idToL={};
# global LisupLoadTimeLis #上货点到叠箱机的时间序列
dr = {}
r=set()
ans = set();
rrr=[];

LisDdjTime = []
LisDdjTimeD = []
LisInspect = [{'2':[11,17,13]},{'3':[10]},{'4':[10,14]},{'5':[11,11]}]#json 文件中获得
LisReturnTime = []
LisEnterTime = []
inspectIndex = 0
returnIndex = 0
DdjEnterXYZ = []  #[[[ddj1_x1.ddj1_y1,ddj1_z1],[...]],[[ddj2_x1,...],[....]],...[]]
DdjOutXYZ = []  
DirReturnXYZ = {}  
DdjInspectXYZ = []   #[[二楼[堆垛机序号[堆垛机坐标]],[]]]
InspectTypeFloorNum = []
ReadInspectTypeNum = []
#cty model_3
def emu(org,die,tStop=[]): #算法二输出，叠箱机编号，
    # 记录无入边的
    ru = set();
    # 存放上货点
    d0 = set();
    # 存放交通点
    tran = set();
    # 存树边
    ed = {};
    # 存边权
    t = {};
    # org.append([-1,-1,-1,-1]);
    for i in range(0,len(org)):
            ru.add(org[i][2]);
            ed[org[i][1]] = org[i][2];  # ed[起点]=[终点]
            t[org[i][1]]=org[i][3];
    # 找出上货点
    for i in range(0,len(org)):
        if(org[i][1] not in ru):
            d0.add(org[i][1]);
            # tran.add(ed[key]);
    # 假设已有叠箱机编号
    # die = 1;
    # 首交通点 到 叠箱机
    # 直接全算，没算法
    res={};
    for i in d0:
        st = ed[i];
        if(st not in res):
            res[st] = 0;
            j=st;
            while(j!=die):
                res[st]+=t[j];
                #留待加停留时间
                j=ed[j];
    Liscross = [];
    for i in d0:
        tem=[];
        ttm=[];
        tem.append(i);
        tem.append(ed[i]);
        tem.append(t[i]);
        ttm.append(ed[i]);
        ttm.append(die);
        ttm.append(res[ed[i]]);
        Liscross.append([tem,ttm]);
    return Liscross;
###


#model_4
#去重
def delList(L):
    L1 = []
    for i in L:
        if i not in L1:
            L1.append(i)
    return L1

#n个上货点的最短上货频率和资产初始上货时刻
def upLoad():
    
    return 0


#计算上货点的上货频率
def CALCupLoadFre(lostTime,upLoadNum):
    return lostTime*upLoadNum


#找出上货点的对应数标
def CALCupLoadSign(LisCross):
    LisupLoadSign = [] 
    for i in LisCross:
        LisupLoadSign.append(i[0][0])
    return LisupLoadSign

#找出上货点 交汇的所有数标
def CALCupLoadCross(LisCross):
    upLoadCross = []
    for i in LisCross:
        upLoadCross.append(i[0][1])
    upLoadCross = delList(upLoadCross)
    return upLoadCross

#根据上货点的交汇点，将上货点进行分类
def CALCupLoadSameCross(LisCross,upLoadCross):
    LisupLoadSameCross = []
    j = 0
    LisTemp = []
    for i in range(len(upLoadCross)):
        LisupLoadSameCross.append([])
    for j in range(len(upLoadCross)):   
        for i in LisCross:
            if(i[0][1] == upLoadCross[j]):
                LisupLoadSameCross[j].append(i[0])
    return LisupLoadSameCross


#计算各上货点到第一个交汇点的时间
def CALCupLoadFirstCrossTime(LisCross):
    LisUpLoadFirstCrossTime = {}
    j = 0
    for i in LisCross:
        LisUpLoadFirstCrossTime['%d'%j] = i[0][2]
        j += 1
    return LisUpLoadFirstCrossTime

#LisUpLoadFirstCrossTime = CALCupLoadFirstCrossTime(LisCross)#各个上货点到第一个交汇点的时间

#计算各个上货点的初始上货时间
def CALCupLoadTime():
    LisCrossTime = CALCupLoadFirstCrossTime(LisCross)
    LisCrossTime = sorted(LisCrossTime.items(), key=lambda item:item[1], reverse = True) #按照 value 倒序排序
    #LisCrossTime =  sorted(LisCrossTime,reverse=True)
    upLoadNum = len(LisCrossTime)
    upLoadFre = CALCupLoadFre(lostTime,upLoadNum)
    #LisupLoadStartTime = LisCrossTime
    LisupLoadStartTime = []
    #print(LisCrossTime)
    for i in range(upLoadNum):
        #print('i',i)
        if(i==0):
            LisupLoadStartTime.append(0)
        else:
            time_t = (LisCrossTime[i-1][1] + (i) * lostTime) - LisCrossTime[i][1]
            if(time_t <  upLoadFre):
                LisupLoadStartTime.append(time_t)
            else:
                LisupLoadStartTime.append(time_t % upLoadFre)
    dir = {}
    for i in range(upLoadNum):
        dir['%s'%(LisCrossTime[i][0])] = LisupLoadStartTime[i]
    tuple = sorted(dir.items(),key=lambda x:x[0]) #按照key的值正序排序
    LisupLoadStartTime = []
    for i in range(upLoadNum):
        LisupLoadStartTime.append(tuple[i][1])
    return LisupLoadStartTime 


#上货点分配任务量
def CALCupLoadGoodsNum(upLoadNum,LisGoodsNum,mod):
    LisupLoadGoodsNum = []
    LisTemp = []
    #按照上货点数量对列表进行分割
    for i in range(upLoadNum):
        LisupLoadGoodsNum.append([])
    #获取每种资产的上货数量
    for i in LisGoodsNum[0]:
        #print(LisGoodsNum[0][i])
        LisTemp.append(LisGoodsNum[0][i] * mod)
    #针对每种类型的上货资产，在上货点出进行分割
    LisNum = [0]
    upLoadIndex = 0
    
    for j in LisTemp:#第 j 次分割
        LisNum  = []
        LisNum = CALCeachUpLoadNum(upLoadNum=upLoadNum,GoodsNum=j)
        for i in range(upLoadNum):
            LisupLoadGoodsNum[upLoadIndex].append(LisNum[i][0])
            upLoadIndex += 1
            if(upLoadIndex == upLoadNum):
                upLoadIndex = 0
        upLoadIndex = LisNum[len(LisNum)-1]
    #print(LisupLoadGoodsNum)
    return LisupLoadGoodsNum

#根据上货点数量和货物数量对每个上货点的上货量进行分割
def CALCeachUpLoadNum(upLoadNum,GoodsNum):
    LisNum = []
    for i in range(upLoadNum):
        LisNum.append([])
    upLoadIndex = 0#记录开始上货点的标号
    eachNum = int(GoodsNum/upLoadNum)
    temp = GoodsNum%upLoadNum
    
    for i in range(upLoadNum):
        LisNum[i].append(eachNum)
    if(temp == 0): #如果可以平均分
        LisNum.append(upLoadIndex)
        return LisNum
    else:     #不能平均分  
        for i in range(upLoadNum):
            if(temp==0):
                LisNum.append(upLoadIndex)
                return LisNum
            #temp = GoodsNum%upLoadNum 
            LisNum[upLoadIndex][0] = eachNum + 1
            upLoadIndex += 1
            temp -= 1
    # LisNum.append(upLoadIndex)        
    # return LisNum
    

#做出一个列表 数据结构为 [[startTime,fre,time1,time2],...,]
def CALCupLoadParm(LisCross):
    upLoadNum = len(CALCupLoadFirstCrossTime(LisCross))
    upLoadFre = CALCupLoadFre(lostTime,upLoadNum)
    LisupLoadStartTime = CALCupLoadTime()
    LisupLoadParm = []
    for i in LisupLoadStartTime:
        LisupLoadParm.append([])
    for i in range(upLoadNum):
        LisupLoadParm[i].append(int(LisupLoadStartTime[i]))
        LisupLoadParm[i].append(upLoadFre)
        for j in LisCross[i]:
            LisupLoadParm[i].append(j[2])
    return LisupLoadParm

#货物到达叠箱机的时间序列（按照上货点以及资产类型区分）
def CALCupLoadTimeLis():
    upLoadNum = len(CALCupLoadFirstCrossTime(LisCross))
    LisupLoadStartTime = CALCupLoadTime()
    LisupLoadGoodsNum = CALCupLoadGoodsNum(upLoadNum,LisGoodsNum,mod2)
    LisupLoadParm = CALCupLoadParm(LisCross)
    LisupLoadTimeLis = []
    #创造出与货物类型区分开的列表的数据结构
    for i in range(len(LisupLoadGoodsNum)):
        LisupLoadTimeLis.append([])
        for j in range(len(LisupLoadGoodsNum[i])):
            LisupLoadTimeLis[i].append([])
    for i in range(len(LisupLoadGoodsNum)):
        time = 0
        index = 0
        for n in LisupLoadGoodsNum[i]:
            #k = len((LisupLoadGoodsNum[i]))
            for j in range(n):
                time +=  LisupLoadParm[i][0] + j*LisupLoadParm[i][1] + LisupLoadParm[i][2] + LisupLoadParm[i][3]
                LisupLoadTimeLis[i][index].append(time)
            index += 1
    #print(LisupLoadParm)
    return LisupLoadTimeLis

#货物到达叠箱机的时间序列(总时间序列)
def CALCupLoadAllTimeLis():
    upLoadNum = len(CALCupLoadFirstCrossTime(LisCross))
    LisupLoadStartTime = CALCupLoadTime()
    LisupLoadGoodsNum = CALCupLoadGoodsNum(upLoadNum,LisGoodsNum,mod2)
    LisupLoadParm = CALCupLoadParm(LisCross)
    LisupLoadTimeLis = []
    for i in range(len(LisupLoadGoodsNum)):
        #遍历两个上货点
        time = 0
        index = 0
        upLoadTotalNum = 0
        for j in LisupLoadGoodsNum[i]:
            upLoadTotalNum += j
        for j in range(upLoadTotalNum):
            time =  LisupLoadParm[i][0] + j*LisupLoadParm[i][1] + LisupLoadParm[i][2] + LisupLoadParm[i][3]
            time = round(time,3)
            LisupLoadTimeLis.append(time)
        # for n in LisupLoadGoodsNum[i]:
        #     #k = len((LisupLoadGoodsNum[i]))
        #     for j in range(n):
        #         #何时上货： 1:LisupLoadParm[i][0]  2:LisupLoadParm[i][0] + LisupLoadParm[i][1] 3:LisupLoadParm[i][0] + 2*LisupLoadParm[i][1]
        #         time =  LisupLoadParm[i][0] + j*LisupLoadParm[i][1] + LisupLoadParm[i][2] + LisupLoadParm[i][3]
        #         LisupLoadTimeLis.append(time)
        #     index += 1
        
    #print(LisupLoadParm)
    LisupLoadTimeLis = sorted(LisupLoadTimeLis)
    return LisupLoadTimeLis


####

def getLine():
    global rrr
    global ans
    ans = set()
    rs = [];

    #取出所有货架编号
    for i in range(0,len(CargoNow)):
        ans.add(CargoNow[i]['line']);
    #取出集合所有元素放入list
    for i in ans:
        rs.append(i);
    #list排序
    # rs=[3,4,5,6,7,8,9,10,11,12,13,14,16];
    rs.sort()
    # print("%%%%%%%%%%%%%%")
    # print(rs)
    # print("%%%%%%%%%%%%%%")
    # rs=[1,3,4,5,7,9,11,12,13]

    le = len(rs)
    i=0;
    while(i < le):
        if(i==le-1):
            rrr.append([rs[i]])
            i+=1;
            continue;
        if(rs[i] + 1 == rs[i+1]):
            rrr.append([rs[i],rs[i+1]]);
            i+=2;
        else:
            rrr.append([rs[i]])
            i+=1;

    return rrr;


# global r
# r=set()
def cal(LisCode, n=5):
    global LineTimeList
    global ans
    ans = set()
    #取出所有货架编号
    for i in range(0,len(CargoNow)):
        ans.add(CargoNow[i]['line']);
    LisupLoadTimeLis = CALCupLoadAllTimeLis()  # 上货点到叠箱机
    #print("LisupLoadTimeLis", LisupLoadTimeLis)
    dList = {};
    line = list(ans)
    line.sort()
    global r
    global dr
    
    if (len(r) == 0 or len(dr) == 0):
        for i in range(0, len(CargoNow)):
            if (CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 0):
                r.add(CargoNow[i]['num'])
                # r[res[i]['num']]=int(res[i]['type']);
                dr[CargoNow[i]['num']] = int(CargoNow[i]['line']);

    rTot = [];
    for i in LisCode:
        if (i in r):
            rTot.append(i);

    # 检验箱之间安全间隔时间是否满足
    nn = n;
    for i in range(1, len(LisupLoadTimeLis)):
        diff = LisupLoadTimeLis[i] - LisupLoadTimeLis[i - 1];
        tem = (i + 1) % nn;
        if (tem == 0):
            if (diff < 4):
                LisupLoadTimeLis[i] = LisupLoadTimeLis[i - 1] + 4;
                continue;
        if (diff < 9):
            LisupLoadTimeLis[i] = LisupLoadTimeLis[i - 1] + 9;

    # 处理list
    LineTimeList.reverse();
    LineTimeList.append(LineTimeList[-1]);
    # 在sort后获取line
    for i in range(0, len(line)):
        dList[line[i]] = LineTimeList[i];
    rres = [];
    le = len(LisupLoadTimeLis);
    rest = le % n;
    cnt = 0;
    temp_i = 0
    global lineToDdj
    if(len(lineToDdj)==0):
        if(len(rrr) == 0):
            getLine()
        for i in range(0,len(rrr)):
            for j in range(0,len(rrr[i])):
                lineToDdj[rrr[i][j]] = (i+1);
    for i in range(4, le, 5):
        rres.append({})
        ttem = LisupLoadTimeLis[i] + dList[dr[rTot[cnt]]];
        rres[temp_i]['%d'%(lineToDdj[dr[rTot[cnt]]])] = round(ttem,3)
        cnt += 1;
        temp_i += 1
    # 保留小数点后两位
    # for i in range(len(rres)):
    #     rres[i] = round(rres[i], 3)
    #这里得改下，rres是个字典,rres[时间]=堆垛机编号
    # 最后的不满5箱的
    # if(rest!=0):
    #print(RefResolutionError)
    temp = []
    for i in range(len(rres)):
        for j in rres[i]:
            temp.append(int(j))
    temp = DelList(temp)
    temp2 = []
    for i in range(len(temp)):
        temp2.append([])
    for i in range(len(rres)):
        for j in rres[i]:
            temp2[int(j)-1].append(rres[i])
    #print(temp2)
    rres = temp2
    # ddj = 1
    # print(rres[ddj-1][0].get('%d'%(ddj)))
    return rres;


####model_4 over


#####model_1####

#判断编码属于的堆垛机序号




def CALCStacker(id):
    global rrr
    global lineToDdj
    global idToL
    #rrr是否为空
    if(len(rrr)==0):
        getLine();
    #lineToDdj是否为空
    if(len(lineToDdj)==0):
        for i in range(0,len(rrr)):
            for j in range(0,len(rrr[i])):
                lineToDdj[rrr[i][j]] = (i+1);

    #idToL是否为空
    if(len(idToL)==0):
        for i in range(0, len(CargoNow)):
            idToL[CargoNow[i]['num']] = CargoNow[i]['line']
        # dat({},{},{},{},set(),0);    
        for i in idToL:
            tem = lineToDdj[idToL[i]];
            idToL[i] = tem;

    if(id==-1):
        return 0
    
    return idToL[id];


def getLisDdjCode(rdLi):
    Nddj=len(getLine());
    
    # if(len(rdLi)==0):
    #     r = {}
    #     h = {}
    #     s = {}
    #     c = {}
    #     # 获取字典 r,h,s,c
    #     tt=set();#无用
    #     dd={};#wuyo
    #     n = dat(r, h, s, c,dd,tt);
    #     rdLi = rdCode(len(n));
    # print(rdLi)
    # print(Nddj)
    output = [];
    for i in range(0,Nddj):
        output.append([]);
    for i in rdLi:
        dN = CALCStacker(i);
        output[dN-1].append(i);

    return output;


#######
#global inspectIndex #已检定个数

#去重
def DelList(L):
    L1 = []
    for i in L:
        if i not in L1:
            L1.append(i)
    return L1

#判断编码类型函数
def CALCjudgeType(p):
    type = '0'
    if(CargoNow[p-1]['s1'] == 0 and CargoNow[p-1]['s2'] == 0):
        type = 'R'
    elif(CargoNow[p-1]['s1'] == 0 and CargoNow[p-1]['s2'] == 1):
        type = 'S'
    elif(CargoNow[p-1]['s1'] == 1 and CargoNow[p-1]['s2'] == 0):
        type = 'H'
    elif(CargoNow[p-1]['s1'] == 1 and CargoNow[p-1]['s2'] == 1):
        type = 'C'
    return type

#编码处理，送检在回库之前
#编码按照堆垛机分开
#LisDdjCode = [[39, 59, 12, 64, 68, 45, 31, 29, 84, 61, 50, 37, 77, 81, 47], [8, 71, 65, 51, 34, 28, 56, 6, 69, 43, 1, 42, 3, 57], [9, 75, 55, 11, 5, 41, 67, 53, 78, 21], [76, 60, 58, 80, 83, 24, 46, 35, 44], [70, 30, 74, 54, 48, 36, 66, 73, 49, 79, 18, 72, 52, 19, 40, 62, 32, 63], [2, 14, 22, 82, 4, 20, 13, 26, 33, 15, 10, 27, 23, 38, 25, 16, 17, 7]]

#将送检和回库编码取出，按照堆垛机,并将送检编码提前到相对应的回库编码之前
def GetS_H(LisDdjCode):
    global LisReturnTime
    for i in range(len(LisDdjCode)):
        for j in range(len(LisDdjCode[i])):
            if(CALCjudgeType(LisDdjCode[i][j]) == 'S'):
                for k in range(len(LisDdjCode[i])):
                    if((LisDdjCode[i][j]-S) == LisDdjCode[i][k]):
                        if(k<j):
                            temp = LisDdjCode[i][j]
                            LisDdjCode[i][j] = LisDdjCode[i][k]
                            LisDdjCode[i][k] = temp
    LisS_H = []
    for i in range(len(LisDdjCode)):
        LisS_H.append([])
        LisS_H[i].append([])
        LisS_H[i].append([])
    LisTemp_S = []
    for i in range(len(LisDdjCode)):
        for j in range(len(LisDdjCode[i])):
            if(CALCjudgeType(LisDdjCode[i][j]) == 'S'):
                LisTemp_S.append(LisDdjCode[i][j])
                LisS_H[i][0].append(LisDdjCode[i][j])
            elif(CALCjudgeType(LisDdjCode[i][j]) == 'H'):
                LisS_H[i][1].append(LisDdjCode[i][j])
    for i in range(S):
        LisReturnTime.append([])
        LisReturnTime[i] = {}
    #初始化LisReturn
    for i in range(len(LisReturnTime)):
        LisReturnTime[i]['%d'%(LisTemp_S[i])] = float('inf') 
    #print(LisDdjCode)
    #print(LisS_H)
    #print(LisReturnTime)
    return LisS_H
#GetS_H(LisDdjCode)



#堆垛机行走时间
def CALCWalkTime(x,y):
    v1 = 0.5  #堆垛机垂直移动速度
    v2 = 10   #堆垛机水平移动速度
    HighRoad = 0  #垂直移动的距离
    LongRoad = 0  #水平移动的距离
    TimeHighRoad = 0 #垂直移动的时间
    TimeLongRoad = 0 #水平移动的时间
    TimeRunRoad = 0  #堆垛机移动的时间
    HighRoad = y 
    LongRoad = x
    TimeHighRoad = y / v1  #计算垂直移动的时间
    TimeLongRoad = x / v2  #计算水平移动的时间
    TimeRunRoad = max(TimeHighRoad,TimeLongRoad)  #计算堆垛机的时间
    return TimeRunRoad


#根据编码，获得堆垛机的上货点的坐标
def GetEnterXY(p):
    ddj = CALCStacker(p)
    LisEnterXY = DdjEnterXYZ[ddj-1]
    
    return LisEnterXY 
'''
    "floor2": [ 11, 17, 13 ],
    "floor3": [ 10 ],
    "floor4": [ 10, 14 ],
    "floor5": [ 11, 11 ]
'''


#处理数据
def AddLisInspect():
    global LisInspect
    LF = []
    for i in range(len(LisInspect)):
        LF.append([])
        L = []
        L = LisInspect[i].keys()
        LF[i] = int(list(L)[0])
    for i in range(len(LisInspect)):
        L = list(LisInspect[i].values())
        for j in range(len(L[0])):
            if(L[0][j] == 11):
                LisInspect[i]['%d'%(LF[i])].append(15)
                LisInspect[i]['%d'%(LF[i])].append(16)
    for i in range(len(LisInspect)):
        L = list(LisInspect[i].values())
        for j in range(len(L[0])):
            LisInspect[i]['%d'%(LF[i])] = DelList(LisInspect[i]['%d'%(LF[i])] )
    return LisInspect
# LisInspect = AddLisInspect(LisInspect)
#print("LisInspect",LisInspect)
#根据楼层划分资产类型
def CALCDayInspectFloor():
    global LisInspect
    LisInspect = AddLisInspect()
    LisT = []
    LisF = []
    for i in range(len(CargoNow)):
        if(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 1):
            LisT.append(CargoNow[i]['type'])
    LisT = DelList(LisT)
    L = []
    for i in range(len(LisInspect)):
        LisF.append([])
        LisF[i] = {}
        L1 = LisInspect[i].keys()
        L1 = list(L1)
        L.append(int(L1[0]))
        LisF[i]['%d'%(L[i])] = []
        L1 = LisInspect[i].values()
        L1 = list(L1)
        for k in range(len(LisT)):
            for j in L1[0]:
                #print(LisT[k])
                if LisT[k] == j:
                    LisF[i]['%d'%(L[i])].append(j)  
        for j in range(len(LisF[i]['%d'%(L[i])])):
            LisF[i]['%d'%(L[i])].append(100/len(LisF[i]['%d'%(L[i])])) 

    #print("LisF",LisF)  #计算当日送检楼层实际检定的资产型号序列
    return LisF
# LisF = CALCDayInspectFloor()

#根据类型划分楼层
def CALCDayInspectType():
    global LisInspect
    List = []
    LisT = []
    for i in range(len(CargoNow)):
        if(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 1):
            List.append(CargoNow[i]['type'])
    List = DelList(List)
    #print(List)
    #准备好字典
    for i in range(len(List)):
        LisT.append([])
        LisT[i] = {}
        LisT[i]['%d'%(List[i])] = []
    #print(LisT)
    #获取所有楼层
    LF = []
    for i in range(len(LisInspect)):
        LF.append([])
        L = []
        L = LisInspect[i].keys()
        LF[i] = int(list(L)[0])
    #print(LF)
    #计算当日送检资产型号的楼层序列
    for i in range (len(List)):
        for j in range(len(LisInspect)):
            for k in LisInspect[j]['%d'%(LF[j])]:
                if k == List[i]:
                    LisT[i]['%d'%(List[i])].append(LF[j])
    #print("LisT",LisT)
    return LisT
#LisT = CALCDayInspectType()
#print(LisT)
dirInspect = {'10':8,'15':6}
#分配当日送检资产的楼层权重：
def CALCDayInspectIW():
    global InspectTypeFloorNum 
    LisF = CALCDayInspectFloor()
    LisT = CALCDayInspectType()
    global LisInspect
    List  = []
    for i in range(len(CargoNow)):
        if(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 1):
            List.append(CargoNow[i]['type'])
    List = DelList(List)
    LF = []
    for i in range(len(LisInspect)):
        LF.append([])
        L = []
        L = LisInspect[i].keys()
        LF[i] = int(list(L)[0])
    L = []
    for i in range(len(LisF)):
        L.append([])
        L[i] = {}
        L[i]['%d'%(LF[i])] = LisF[i]['%d'%(LF[i])][-1]
        #print(LisF[i]['%d'%(LF[i])][-1])
    LisT_GoodNUm =  copy.deepcopy(LisT)
    for i in range(len(LisT)):
        for j in range(len(LisT[i]['%d'%(List[i])])):
                temp = LisT[i]['%d'%(List[i])][j]
                LisT[i]['%d'%(List[i])][j] = {}
                LisT[i]['%d'%(List[i])][j]['%d'%(temp)] = 0
                
    # print("LisT_GoodNUm",LisT_GoodNUm)        
    # print("LisT",LisT)
    # temp = LisT[0].get('10')[0] 
    # LisT[0].get('10')[0]  = {}
    # LisT[0].get('10')[0]['%d'%(temp)] = 0
    # print(LisT[0].get('10'))
    
    for i in range(len(LisT_GoodNUm)):
        for j in range(len(LisT_GoodNUm[i]['%d'%(List[i])])):
            for m in range(len(LisF)):
                for k in L[m]:
                    # print("LisT[i]['%d'%(List[i])][j]",LisT[i]['%d'%(List[i])][j])
                    # print("k",k)
                    if( int(k) == int(LisT_GoodNUm[i]['%d'%(List[i])][j])):
                        LisT_GoodNUm[i]['%d'%(List[i])][j] = int(L[m].get('%s'%(k)))
    #print("LisT_k",LisT_GoodNUm)
    LisNum = []
    for i in range(len(List)):
        temp = 0
        for j in range(len(LisT_GoodNUm[i]['%d'%(List[i])])):
            temp += LisT_GoodNUm[i]['%d'%(List[i])][j]
        for j in range(len(LisT_GoodNUm[i]['%d'%(List[i])])):
            LisT_GoodNUm[i]['%d'%(List[i])][j] = LisT_GoodNUm[i]['%d'%(List[i])][j] / temp
            LisT_GoodNUm[i]['%d'%(List[i])][j] = round(LisT_GoodNUm[i]['%d'%(List[i])][j] * dirInspect.get('%d'%(List[i])))
            LisNum.append(LisT_GoodNUm[i]['%d'%(List[i])][j])
    #LisNum = [1,2,3,4]
    #print("LisNum",LisNum)
    Num_p = 0
    for i in range(len(LisT)):
        for k in range(len(LisT[i].get('%d'%(List[i])))):
            for u in LisT[i].get('%d'%(List[i]))[k]:
                LisT[i].get('%d'%(List[i]))[k]['%d'%(int(u))] = LisNum[Num_p]
                Num_p += 1
    global ReadInspectTypeNum
    ReadInspectTypeNum = {}
    for i in range(len(LisT)):
        ReadInspectTypeNum['%d'%(List[i])] = 0
    for i in range(len(LisT)):
        Len = len(LisT[i].get('%d'%(List[i])))
        for j in range(Len):
            if len(LisT[i].get('%d'%(List[i]))) == 1:
                break
            LisT[i].get('%d'%(List[i]))[0] = dict(LisT[i].get('%d'%(List[i]))[0],**LisT[i].get('%d'%(List[i]))[j])
        while True:
            if(len(LisT[i].get('%d'%(List[i])))>1):
                del(LisT[i].get('%d'%(List[i]))[-1])
            else:
                break
            
    #print(ReadInspectTypeNum)
    #print(LisT)
    # print("L",L)
    #print("LisT_GoodNUm",LisT_GoodNUm)
    InspectTypeFloorNum = LisT
    return LisT
#LisT = CALCDayInspectIW() 
#根据堆垛机编码和楼层号，返回堆垛机的送检/回库口
def GetLisInspectXY(ddj,floor):
    global DdjInspectXYZ  #[[二楼[堆垛机序号[堆垛机坐标]],[]]]
    #print(DdjInspectXYZ[floor-2][ddj-1])
    return DdjInspectXYZ[floor-2][ddj-1]


#根据编码，获得堆垛机送检口的坐标
def GetInspectXY(p,Flag):
    global DirReturnXYZ
    global InspectTypeFloorNum
    global ReadInspectTypeNum
    if(CALCjudgeType(p) == 'H'):
        return DirReturnXYZ['%d'%(p+S)]
    type_p = CALCjudgeType(p)
    if(len(InspectTypeFloorNum) == 0):
        CALCDayInspectIW() 
    # print("DdjInspectXYZ",DdjInspectXYZ)
    # print("InspectTypeFloorNum",InspectTypeFloorNum)
    ddj = CALCStacker(p)
    LisInspectXY = [1000,1000]
    Model = CargoNow[p-1]['type']
    p_Floor = 0
    
    # for i in range(len(InspectTypeFloorNum)):
    #     for j in InspectTypeFloorNum[i]:
    #         if int(j) == int(Model):
                
    #             InspectTypeFloorNum[i].get('%d'%(int(j)))
    #             print(InspectTypeFloorNum[i].get('%d'%(int(j))))
    for i in range(len(InspectTypeFloorNum)):
        for j in InspectTypeFloorNum[i]:
            if int(j) == int(Model):
                temp = InspectTypeFloorNum[i].get('%d'%(int(j)))
    presentNum = 0
    for i in temp[0]:
        Num = ReadInspectTypeNum.get('%d'%(Model)) 
        #print(temp[0])
        if(Num - presentNum < temp[0].get('%d'%(int(i)))):
            p_Floor = int(i)
            Num += 1
            ReadInspectTypeNum['%d'%(Model)] = Num
            break
        else:
            presentNum = temp[0].get('%d'%(int(i)))
    if(Flag == False):
        tempNum = ReadInspectTypeNum['%d'%(Model)]
        tempNum -= 1
        ReadInspectTypeNum['%d'%(Model)] = tempNum
    LisInspectXY = GetLisInspectXY(ddj,p_Floor)
    #print("temp",temp)
    if(type_p == 'S'):
        DirReturnXYZ['%d'%(p)] = LisInspectXY
    return LisInspectXY

#根据两个编码判断送检/回库口是否相同
def GetSameFlag(p,second_p):
    if(CALCjudgeType(p) == 'H'):
        for i in LisReturnTime[0]:
            p = int(i)
        for i in LisReturnTime[1]:
            second_p = int(i)
    LisP = GetInspectXY(p,False)
    LisSecond_P = GetInspectXY(second_p,False)
    if(LisP[1] == LisSecond_P[1]):
        SameFlag = True
    else:
        SameFlag = False
    
    return SameFlag

#根据编码，获得堆垛机的出库坐标
def GetOutXY(p):
    ddj = CALCStacker(p)
    LisOutXY = DdjOutXYZ[ddj-1]    
    return LisOutXY
#根据编码计算检定时间
"""
单相表:30min --- 1800
三相表:3h45min --- 10800 + 2700 = 13500
互感器:30min --- 1800
采集终端:4h --- 14400
HPLC:15min --- 900
"""
def GetInspectTime(p):
    if(CargoNow[p-1]['type'] == 11 or CargoNow[p-1]['type'] == 15 or CargoNow[p-1]['type'] == 16):#三相表
        inspectTime = 13500
    elif(CargoNow[p-1]['type'] == 10):#单相表
        inspectTime = 1800
    elif(CargoNow[p-1]['type'] == 13):#互感器
        inspectTime = 1800
    elif(CargoNow[p-1]['type'] == 10):#采集终端
        inspectTime = 14400
    elif(CargoNow[p-1]['type'] == 17 or CargoNow[p-1]['type'] == 18 or CargoNow[p-1]['type'] == 19):#HPLC
        inspectTime = 900
    #elif()
    else:
        print("GetInspectTime Error!")
        inspectTime = 900
    return inspectTime

#回库编码的排序
def sortReturnCode():
    global LisReturnTime
    for i in range(0,len(LisReturnTime)):
        for j in range(0,len(LisReturnTime)-i-1):
            if round(list(LisReturnTime[j].values())[0],3) > round(list(LisReturnTime[j+1].values())[0],3):
                temp = LisReturnTime[j+1]
                LisReturnTime[j+1] = LisReturnTime[j]
                LisReturnTime[j] = temp

#计算回库编码的等待时间
def CALCReturnWaitTime(p,TI):
    global LisReturnTime
    waitTime = 0
    returnTime = 0
    # tempI = 0
    # temp = 0
    # for i in range(len(LisReturnTime)):
    #     for j in LisReturnTime[i]:
    #         #print(j)
    #         if(p+S == int(j)):
    #             temp = int(j)
    #             tempI = i
    #             break
    #     if(temp > 0):
    #         break
    # print(LisReturnTime[i])
    # print(LisReturnTime[i].get('%d'%(temp)))
    #returnTime = int(LisReturnTime[i].get('%d'%(temp)))
    returnTime = round(list(LisReturnTime[0].values())[0],3)
    LisReturnTime[0] = {}
    LisReturnTime[0]['已读'] = float('inf') 
    sortReturnCode()
    if(returnTime > int(TI)):
        waitTime = returnTime - TI
    else:
        waitTime = 0
    return waitTime

#计算入库的等待时间
def GetEnterWaitTime(p,TI):
    global LisEnterTime
    ddj = CALCStacker(p)
    enterTime = LisEnterTime[ddj-1][0].get('%d'%(ddj))
    del LisEnterTime[ddj-1][0] 
    if(enterTime > TI):
        return enterTime
    else:
        return 0
#读码函数
def ReadCode(TI,TDI,p,second_p,third_p):
    global LisReturnTime
    #编码类型
    p_type = '0'
    second_p_type = '0'
    third_p_type = '0'
    
    TwoFlag = False #是否一次取两垛
    SameFlag = False #送检/回库 口 是否相同
    
    ddj = 0  # 堆垛机序号
    
    waitTime = 0    #堆垛机等待时长
    grabTime = 20  #取货时长
    placeTime = 20 #卸货时长
    walkTime1 = 0   #行走时长1
    walkTime2 = 0   #行走时长2
    walkTime3 = 0   #行走时长3
    walkTime4 = 0   #行走时长4
    
    
    p_type = CALCjudgeType(p) #获取编码p的类型
    second_p_type = CALCjudgeType(second_p) #获取编码second_p的类型
    #回库编码的变化
    if(p_type == 'H'):
        if(second_p == 'H'):
            for i in LisReturnTime[0]:
                p = int(i) - S
            for i in LisReturnTime[1]:
                second_p = int(i) - S
        else:
            for i in LisReturnTime[0]:
                p = int(i) - S
    p_type = CALCjudgeType(p) #获取编码p的类型
    second_p_type = CALCjudgeType(second_p) #获取编码second_p的类型
    third_p_type = CALCjudgeType(third_p)   #获取编码third_p的类型
    ddj = CALCStacker(p)    #获取编码p的堆垛机序号
    
    if(second_p > 0 and third_p == -1): #第三个编码为-1，前两个为一般编码
        third_p_type = 'R'
    elif(second_p == -1 and third_p == -1):#后两个编码都为-1
        second_p_type = -1
        third_p_type = 'R'
        pass
    #判断p与second_p是否为同种类型
    if(p_type == second_p_type):
        #一次作业两垛资产 类型相同
        TwoFlag = True
        if(p_type=='R'):
            #入库 放两垛资产
            first_x = CargoNow[p-1]['x']
            first_y = CargoNow[p-1]['y']
            
            second_x = CargoNow[second_p-1]['x']
            second_y = CargoNow[second_p-1]['y']
        elif(p_type=='S'):
            SameFlag = GetSameFlag(p,second_p)
            if(SameFlag == True):
                #送检口相同
                #去第二个货位取货
                first_x = CargoNow[second_p-1]['x']
                first_y = CargoNow[second_p-1]['y']
                #送检口
                LisInspectXY = GetInspectXY(p,True)
                LisInspectXY = GetInspectXY(second_p,True)
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                second_x = inspectX
                second_y = inspectY 
                pass
            else:
                #送检口不同
                #去第二个货位取货
                first_x = CargoNow[second_p-1]['x']
                first_y = CargoNow[second_p-1]['y']
                #p的送检口
                LisInspectXY = GetInspectXY(p,True)
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                second_x = inspectX
                second_y = inspectY 
                #second_p的送检口
                LisInspectXY = GetInspectXY(second_p,True)
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                third_x = inspectX
                third_y = inspectY
                pass
            pass
        elif(p_type == 'H'):
            SameFlag = GetSameFlag(p,second_p)
            if(SameFlag == True):
                #回库口相同，当前堆垛机处于回库口，取两垛货物，从回库口移动到货位1，放一垛货
                first_x = CargoNow[p-1]['x']
                first_y = CargoNow[p-1]['y']
                #堆垛机从货位1移动到货位2，放一垛货
                second_x = CargoNow[second_p-1]['x']
                second_y = CargoNow[second_p-1]['y']
                pass
            else:
                #回库口不同，当前堆垛机处于第一个回库口，取一垛货物，之后从回库口1移动到回库口2
                #获取回库口2的坐标
                LisInspectXY = GetInspectXY(second_p,False)
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                first_x = inspectX
                first_y = inspectY
                #回库口2取一垛货，之后移动到货位1
                second_x = CargoNow[p-1]['x']
                second_y = CargoNow[p-1]['y']
                #在货位1放一垛货，之后移动到货位2
                third_x = CargoNow[second_p-1]['x']
                third_y = CargoNow[second_p-1]['y']
                pass
            pass
        elif(p_type == 'C'):
            #堆垛机当前位于货位1，取一垛货，移动到货位2
            first_x = CargoNow[second_p-1]['x']
            first_y = CargoNow[second_p-1]['y']
            #堆垛机从货位2移动到出库口
            LisOutXY = GetOutXY(p)
            outX = LisOutXY[0]
            outY = LisOutXY[1]
            second_x = outX
            second_y = outY
        else:
            print("ReadCode p_type TwoFlag = True Error!")
    else:
        TwoFlag = False
        if(p_type == 'R'):
            #入库 堆垛机当前在入库口，取一垛资产
            #堆垛机从入库口移动到货位1，放一垛货
            first_x = CargoNow[p-1]['x']
            first_y = CargoNow[p-1]['y']
        elif(p_type == 'S'):
            #送检，堆垛机当前在货位，取一垛货，移动到送检口放货
            LisInspectXY = GetInspectXY(p,True)
            inspectX = LisInspectXY[0]
            inspectY = LisInspectXY[1]
            first_x = inspectX
            first_y = inspectY
        elif(p_type == 'H'):
            #回库，堆垛机当前在回库口，取一垛货，移动到货位放货
            first_x = CargoNow[p-1]['x']
            first_y = CargoNow[p-1]['y']
        elif(p_type == 'C'):
            #出库，当前在货位，需要移动到出库口
            LisOutXY = GetOutXY(p)
            outX = LisOutXY[0]
            outY = LisOutXY[1]
            first_x = outX
            first_y = outY
        else:
            print("ReadCode p_type TwoFlag = False Error!")
            
    #判断最后一个编码的类型，确定堆垛机最后一步要移动到的位置
    if(TwoFlag == False):
        third_p = second_p
        third_p_type = second_p_type
    if(third_p_type == 'R'):
        LisEnterXY = GetEnterXY(third_p)
        enterX = LisEnterXY[0]
        enterY = LisEnterXY[1]
        last_x = enterX
        last_y = enterY
    elif(third_p_type == "S" or third_p_type == 'C'):
        last_x = CargoNow[third_p-1]['x']
        last_y = CargoNow[third_p-1]['y']
    elif(third_p_type == 'H'):
        LisInspectXY = GetInspectXY(third_p,False)
        inspectX = LisInspectXY[0]
        inspectY = LisInspectXY[1]
        last_x = inspectX
        last_y = inspectY  
    elif(third_p_type == -1):
        LisEnterXY = GetEnterXY(p)
        enterX = LisEnterXY[0]
        enterY = LisEnterXY[1]
        last_x = enterX
        last_y = enterY
    else:
        print("ReadCode third_x Error!")
    #读码
    if(p_type=='R'):
        #判断入库口的堵塞问题
        # if(CargoNow[p-1]['flag'] == 'A'):
        #     firstFlag = 0
        # elif(CargoNow[p-1]['flag'] == 'B'):
        #     firstFlag = 1
        if(TwoFlag == True):
            LisEnterXY = GetEnterXY(p)
            enterX = LisEnterXY[0]
            enterY = LisEnterXY[1]
            #一次入库两垛
            #放到货位1上
            walkTime1 = CALCWalkTime(abs(enterX - first_x),abs(enterY - first_y))
            #放到货位2上
            walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
            #根据third编码类型，移动到初始位置
            walkTime3 = CALCWalkTime(abs(second_x - last_x),abs(second_y - last_y))
            #计算时间
            waitTime1 = GetEnterWaitTime(p,TI)
            waitTime2 = GetEnterWaitTime(second_p,TI)
            waitTime = waitTime1 + waitTime2
            TI += waitTime + grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
            TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
        else:
            #只入库一垛
            LisEnterXY = GetEnterXY(p)
            enterX = LisEnterXY[0]
            enterY = LisEnterXY[1]
            #入库口移动到货位
            walkTime1 = CALCWalkTime(abs(enterX - first_x),abs(enterY - first_y))
            #货位移动到下个编码初始位置
            walkTime2 = CALCWalkTime(abs(first_x - last_x),abs(first_y - last_y))
            #计算时间
            TI += waitTime + grabTime + walkTime1 + walkTime2 + placeTime
            TDI += grabTime + walkTime1 + walkTime2 + placeTime
    elif(p_type=='S'):
        global inspectIndex
        if(TwoFlag == True):
            #SameFlag = GetSameFlag(p,second_p)
            if(SameFlag == True):
                #当前堆垛机已在资产p位置上，首先是取货，之后移动到second_p的货位上
                walkTime1 = CALCWalkTime(abs(CargoNow[p-1]['x'] - first_x),abs(CargoNow[p-1]['y'] - first_y))
                #送检口相同,从货位2走到送检口，放货
                walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
                #从送检口走到下一个编码的起始位置
                walkTime3 = CALCWalkTime(abs(second_x - last_x),abs(second_y - last_y))
                #计算时间
                TI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
                TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
                #保留回库时间
                
                inspectTime = GetInspectTime(p)
                LisReturnTime[inspectIndex] = {}
                LisReturnTime[inspectIndex]['%d'%(p)] = round((TI - walkTime3  + inspectTime),3)
                inspectIndex += 1
                inspectTime = GetInspectTime(second_p)
                LisReturnTime[inspectIndex] = {}
                LisReturnTime[inspectIndex]['%d'%(second_p)] = round((TI - walkTime3 + inspectTime + 1),3)
                inspectIndex += 1
                #对回库时间排序
                sortReturnCode()
                pass
            else:
                #当前堆垛机已在资产p位置上，首先是取货，之后移动到second_p的货位上
                walkTime1 = CALCWalkTime(abs(CargoNow[p-1]['x'] - first_x),abs(CargoNow[p-1]['y'] - first_y))
                #送检口不同
                #送检口不同,从货位2走到送检口1，放货
                walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
                #送检口不同，从送检口1走到送检口2，放货
                walkTime3 = CALCWalkTime(abs(second_x - third_x),abs(second_y - third_y))
                #从送检口2走到下一个编码的起始位置
                walkTime4 = CALCWalkTime(abs(third_x - last_x),abs(third_y - last_y))
                #计算时间
                TI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 + walkTime4
                TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 + walkTime4
                #global inspectIndex
                inspectTime = GetInspectTime(p)
                LisReturnTime[inspectIndex] = {}
                LisReturnTime[inspectIndex]['%d'%(p)] = round((TI - walkTime4 - walkTime3  + inspectTime),3)
                inspectIndex += 1
                inspectTime = GetInspectTime(second_p)
                LisReturnTime[inspectIndex] = {}
                LisReturnTime[inspectIndex]['%d'%(second_p)] = round((TI - walkTime4 + inspectTime),3)
                inspectIndex += 1
                #对回库时间排序
                sortReturnCode()
                pass
            pass
        else:
            #当前位置在货位，移动到送检口
            walkTime1 = CALCWalkTime(abs(CargoNow[p-1]['x'] - first_x),abs(CargoNow[p-1]['y']))
            #从送检口移动到下个编码初始位置
            walkTime2 = CALCWalkTime(abs(first_x - last_x),abs(first_y - last_y))
            #计算时间
            TI += waitTime + grabTime + walkTime1 + walkTime2 + placeTime
            TDI += grabTime + walkTime1 + walkTime2 + placeTime
            inspectTime = GetInspectTime(p)
            LisReturnTime[inspectIndex] = {}
            LisReturnTime[inspectIndex]['%d'%(p)] = round((TI - walkTime2 + inspectTime),3)
            inspectIndex += 1
            #对回库时间排序
            sortReturnCode()
            pass
        #print()
    elif(p_type=='H'):
        if(TwoFlag == True):
            #SameFlag = GetSameFlag(p,second_p)
            if(SameFlag == True):
                #连续取两垛，回库口相同
                #获取堆垛机当前的位置，取两垛货
                LisInspectXY = GetInspectXY(p,False)
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                #堆垛机从当前位置移动到货位1，放一垛货
                walkTime1 = CALCWalkTime(abs(inspectX - first_x),abs(inspectY - first_y))
                #从货位1移动到货位2，放一垛货
                walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
                #从货位2移动到下一个编码的起始位置
                walkTime3 = CALCWalkTime(abs(second_x - last_x),abs(second_y - last_y))
                #计算时间
                #等待时间
                waitTime1 = CALCReturnWaitTime(p,TI)
                waitTime2 = CALCReturnWaitTime(second_p,TI)
                waitTime = waitTime1 + waitTime2
                TI += waitTime + grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
                TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
                pass
            else:
                #回库口不同
                #获取堆垛机当前位置，取一垛货
                LisInspectXY = GetInspectXY(p,False)
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                #堆垛机从当前位置移动到回库口2，取一垛货
                walkTime1 = CALCWalkTime(abs(inspectX - first_x),abs(inspectY - first_y))
                #堆垛机从回库口2移动到货位1，放一垛货
                walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
                #堆垛机从货位1移动到货位2，放一垛货
                walkTime3 = CALCWalkTime(abs(second_x - third_x),abs(second_y - third_y))
                #堆垛机从货位2移动到下一个编码的起始位置
                walkTime4 = CALCWalkTime(abs(third_x - last_x),abs(third_y - last_y))
                #计算时间
                waitTime1 = CALCReturnWaitTime(p,TI)
                waitTime2 = CALCReturnWaitTime(second_p,TI)
                waitTime = waitTime1 + waitTime2
                TI += waitTime + grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 + walkTime4
                TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 + walkTime4
                pass
        else:
            #堆垛机当前位于回库口，取一垛货，移动到货位1，放一垛货
            LisInspectXY = GetInspectXY(p,False)
            inspectX = LisInspectXY[0]
            inspectY = LisInspectXY[1]
            walkTime1 = CALCWalkTime(abs(inspectX - first_x),abs(inspectY - first_y))
            #从货位1移动到下个编码起始位置
            walkTime2 = CALCWalkTime(abs(first_x - last_x),abs(first_y - last_y))
            #计算时间
            waitTime = CALCReturnWaitTime(p,TI)
            TI += waitTime + grabTime + walkTime1 + walkTime2 + placeTime
            TDI += grabTime + walkTime1 + walkTime2 + placeTime
            pass
    elif(p_type=='C'):
        if(TwoFlag == True):
            #出两垛货
            #堆垛机当前在货位1，取一垛货之后，移动到货位2
            walkTime1 = CALCWalkTime(abs(CargoNow[p-1]['x'] - first_x),abs(CargoNow[p-1]['y'] - first_y))
            #堆垛机在货位2取一垛货，移动到出库口，放两垛货
            walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
            #堆垛机移动到下一个编码的起始位置
            walkTime3 = CALCWalkTime(abs(second_x - last_x),abs(second_y - last_y))
            #计算时间
            TI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
            TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
            pass
        else:
            #堆垛机当前位于货位，取一垛货，移动到出库口放货
            walkTime1 = CALCWalkTime(abs(CargoNow[p-1]['x'] - first_x),abs(CargoNow[p-1]['y'] - first_y))
            #堆垛机从出库口移动到下个编码初始位置
            walkTime2 = CALCWalkTime(abs(first_x - last_x),abs(first_y - last_y))
            #计算时间
            TI += waitTime + grabTime + walkTime1 + walkTime2 + placeTime
            TDI += grabTime + walkTime1 + walkTime2 + placeTime
            pass
        pass
    else:
        print("ReadCode p_type error!")
    return TI


def Read(LisDdjCode):
    DdjNum = len(LisDdjCode)
    for i in range(DdjNum):
        LisDdjTime.append(0)
        LisDdjTimeD.append(0)
        # LisDdjTimeD[i] = 0
        # LisDdjTime[i] = 0
    # print(LisDdjCode)
    # print(LisDdjCode[3][1])
    # print(LisDdjCode[3][2])
    # print(LisDdjCode[3][3])
    for i in range(DdjNum):
        k = 0
        for j in range(len(LisDdjCode[i])):
            
            if(k+3 <= len(LisDdjCode[i])):
                LisDdjTime[i] =round(ReadCode(LisDdjTime[i],LisDdjTime[i],LisDdjCode[i][k],LisDdjCode[i][k+1],LisDdjCode[i][k+2]),3)
            elif(k+2 == len(LisDdjCode[i])):
                LisDdjTime[i] = round(ReadCode(LisDdjTime[i],LisDdjTime[i],LisDdjCode[i][k],LisDdjCode[i][k+1],-1),3)
            elif(k+1 == len(LisDdjCode[i])):
                LisDdjTime[i] = round(ReadCode(LisDdjTime[i],LisDdjTime[i],LisDdjCode[i][k],-1,-1),3)
            elif(k == len(LisDdjCode[i])):
                break
            if(k+1 == len(LisDdjCode[i])):
                break
            if(CALCjudgeType(LisDdjCode[i][k]) == CALCjudgeType(LisDdjCode[i][k+1])):
                k += 1
            k += 1
# GetS_H(LisDdjCode)
# Read(LisDdjCode)
#print(LisReturnTime)
# print(LisDdjTime)

#获得堆垛机所需数据，主要是坐标
def initCode():
    CargoNow = [{'x': 1869.90466, 'y': 19.9703217, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 3, 'column': 26, 'type': '10', 'id': 'A-7-3-26', 'bidBatch': '', 'factory': '', 'num': 1}, {'x': 1869.26843, 'y': 7.68457127, 'z': 53.2860031, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 2, 'column': 10, 'type': '10', 'id': 'B-16-2-10', 'bidBatch': '', 'factory': '', 'num': 2}, {'x': 1878.222, 'y': 18.434639, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 16, 'column': 24, 'type': '10', 'id': 'B-8-16-24', 'bidBatch': '', 'factory': '', 'num': 3}, {'x': 1881.42786, 'y': 18.434639, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 21, 'column': 24, 'type': '10', 'id': 'A-15-21-24', 'bidBatch': '', 'factory': '', 'num': 4}, {'x': 1900.63, 'y': 19.2024612, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 51, 'column': 25, 'type': '10', 'id': 'A-9-51-25', 'bidBatch': '', 'factory': '', 'num': 5}, {'x': 1889.743, 'y': 16.1310234, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 34, 'column': 21, 'type': '10', 'id': 'A-7-34-21', 'bidBatch': '', 'factory': '', 'num': 6}, {'x': 1898.0625, 'y': 15.3631821, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 47, 'column': 20, 'type': '10', 'id': 'A-15-47-20', 'bidBatch': '', 'factory': '', 'num': 7}, {'x': 1871.82764, 'y': 19.9703979, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 6, 'column': 26, 'type': '10', 'id': 'B-8-6-26', 'bidBatch': '', 'factory': '', 'num': 8}, {'x': 1889.10876, 'y': 1.54167175, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 33, 'column': 2, 'type': '11', 'id': 'B-10-33-2', 'bidBatch': '', 'factory': '', 'num': 9}, {'x': 1868.62036, 'y': 15.3631821, 'z': 53.2860031, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 1, 'column': 20, 'type': '11', 'id': 'B-16-1-20', 'bidBatch': '', 'factory': '', 'num': 10}, {'x': 1878.222, 'y': 19.2024612, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 16, 'column': 25, 'type': '11', 'id': 'A-9-16-25', 'bidBatch': '', 'factory': '', 'num': 11}, {'x': 1890.38525, 'y': 18.434639, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 35, 'column': 24, 'type': '11', 'id': 'B-6-35-24', 'bidBatch': '', 'factory': '', 'num': 12}, {'x': 1892.94763, 'y': 17.6667786, 'z': 53.286, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 39, 'column': 23, 'type': '11', 'id': 'B-16-39-23', 'bidBatch': '', 'factory': '', 'num': 13}, {'x': 1879.50464, 'y': 16.8989182, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 18, 'column': 22, 'type': '11', 'id': 'A-15-18-22', 'bidBatch': '', 'factory': '', 'num': 14}, {'x': 1871.18518, 'y': 6.14884233, 'z': 53.2860031, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 5, 'column': 8, 'type': '13', 'id': 'B-16-5-8', 'bidBatch': '', 'factory': '', 'num': 15}, {'x': 1868.62036, 'y': 8.452438, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 1, 'column': 11, 'type': '13', 'id': 'A-15-1-11', 'bidBatch': '', 'factory': '', 'num': 16}, {'x': 1892.31165, 'y': 10.7560148, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 38, 'column': 14, 'type': '13', 'id': 'A-15-38-14', 'bidBatch': '', 'factory': '', 'num': 17}, {'x': 1874.38452, 'y': 16.1310234, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 10, 'column': 21, 'type': '13', 'id': 'A-13-10-21', 'bidBatch': '', 'factory': '', 'num': 18}, {'x': 1898.70679, 'y': 13.8274679, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 48, 'column': 18, 'type': '13', 'id': 'A-13-48-18', 'bidBatch': '', 'factory': '', 'num': 19}, {'x': 1898.70679, 'y': 11.5238724, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 48, 'column': 15, 'type': '13', 'id': 'A-15-48-15', 'bidBatch': '', 'factory': '', 'num': 20}, {'x': 1882.06409, 'y': 19.9703217, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 22, 'column': 26, 'type': '15', 'id': 'A-9-22-26', 'bidBatch': '', 'factory': '', 'num': 21}, {'x': 1875.02258, 'y': 7.68457127, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 11, 'column': 10, 'type': '15', 'id': 'A-15-11-10', 'bidBatch': '', 'factory': '', 'num': 22}, {'x': 1898.06311, 'y': 18.434639, 'z': 53.286, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 47, 'column': 24, 'type': '15', 'id': 'B-16-47-24', 'bidBatch': '', 'factory': '', 'num': 23}, {'x': 1874.38452, 'y': 16.1310234, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 10, 'column': 21, 'type': '15', 'id': 'A-11-10-21', 'bidBatch': '', 'factory': '', 'num': 24}, {'x': 1870.54688, 'y': 15.3631821, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 4, 'column': 20, 'type': '15', 'id': 'A-15-4-20', 'bidBatch': '', 'factory': '', 'num': 25}, {'x': 1869.26843, 'y': 17.6667786, 'z': 53.286, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 2, 'column': 23, 'type': '15', 'id': 'B-16-2-23', 'bidBatch': '', 'factory': '', 'num': 26}, {'x': 1891.02551, 'y': 13.8274679, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 36, 'column': 18, 'type': '15', 'id': 'A-15-36-18', 'bidBatch': '', 'factory': '', 'num': 27}, {'x': 1884.62317, 'y': 16.1310234, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 26, 'column': 21, 'type': '16', 'id': 'B-8-26-21', 'bidBatch': '', 'factory': '', 'num': 28}, {'x': 1871.18518, 'y': 18.434639, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 5, 'column': 24, 'type': '16', 'id': 'B-6-5-24', 'bidBatch': '', 'factory': '', 'num': 29}, {'x': 1892.31165, 'y': 13.0595894, 'z': 50.35678, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 38, 'column': 17, 'type': '16', 'id': 'B-14-38-17', 'bidBatch': '', 'factory': '', 'num': 30}, {'x': 1882.71045, 'y': 16.1310616, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 23, 'column': 21, 'type': '16', 'id': 'B-6-23-21', 'bidBatch': '', 'factory': '', 'num': 31}, {'x': 1898.0625, 'y': 18.434639, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 47, 'column': 24, 'type': '16', 'id': 'A-13-47-24', 'bidBatch': '', 'factory': '', 'num': 32}, {'x': 1877.58569, 'y': 10.7560148, 'z': 53.2860031, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 15, 'column': 14, 'type': '16', 'id': 'B-16-15-14', 'bidBatch': '', 'factory': '', 'num': 33}, {'x': 1888.46655, 'y': 19.2025337, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 32, 'column': 25, 'type': '16', 'id': 'B-8-32-25', 'bidBatch': '', 'factory': '', 'num': 34}, {'x': 1892.94763, 'y': 13.0595894, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 39, 'column': 17, 'type': '16', 'id': 'B-12-39-17', 'bidBatch': '', 'factory': '', 'num': 35}, {'x': 1882.71045, 'y': 13.0595894, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 23, 'column': 17, 'type': '16', 'id': 'A-13-23-17', 'bidBatch': '', 'factory': '', 'num': 36}, {'x': 1883.3446, 'y': 19.2024975, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 24, 'column': 25, 'type': '16', 'id': 'A-5-24-25', 'bidBatch': '', 'factory': '', 'num': 37}, {'x': 1896.14722, 'y': 8.452438, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 44, 'column': 11, 'type': '16', 'id': 'A-15-44-11', 'bidBatch': '', 'factory': '', 'num': 38}, {'x': 1898.70679, 'y': 19.97036, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 48, 'column': 26, 'type': '16', 'id': 'A-5-48-26', 'bidBatch': '', 'factory': '', 'num': 39}, {'x': 1886.54578, 'y': 17.6667786, 'z': 48.6279373, 's1': 1, 's2': 0, 'flag': 'A', 'line': 13, 'row': 23, 'column': 29, 'type': 10, 'id': 'A-13-29-23', 'bidBatch': '2019年第一批', 'factory': '杭州炬华', 'num': 40}, {'x': 1883.98486, 'y': 8.452438, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 11, 'column': 25, 'type': 10, 'id': 'A-9-25-11', 'bidBatch': '2019年第二批', 'factory': '杭州炬华', 'num': 41}, {'x': 1872.464, 'y': 5.380984, 'z': 42.17527, 's1': 1, 's2': 0, 'flag': 'B', 'line': 8, 'row': 7, 'column': 7, 'type': 10, 'id': 'B-8-7-7', 'bidBatch': '2020年第一批', 'factory': '宁夏隆基', 'num': 42}, {'x': 1871.82764, 'y': 3.84524536, 'z': 42.17527, 's1': 1, 's2': 0, 'flag': 'B', 'line': 8, 'row': 5, 'column': 6, 'type': 10, 'id': 'B-8-6-5', 'bidBatch': '2021年第一批', 'factory': '杭州炬华', 'num': 43}, {'x': 1883.98486, 'y': 17.6667786, 'z': 47.6289978, 's1': 1, 's2': 0, 'flag': 'B', 'line': 12, 'row': 23, 'column': 25, 'type': 10, 'id': 'B-12-25-23', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 44}, {'x': 1876.30713, 'y': 6.14884233, 'z': 38.3443832, 's1': 1, 's2': 0, 'flag': 'B', 'line': 6, 'row': 8, 'column': 13, 'type': 10, 'id': 'B-6-13-8', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 45}, {'x': 1889.10876, 'y': 15.3631821, 'z': 45.8976822, 's1': 1, 's2': 0, 'flag': 'A', 'line': 11, 'row': 20, 'column': 33, 'type': 10, 'id': 'A-11-33-20', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 46}, {'x': 1871.18518, 'y': 15.3632011, 'z': 38.3443832, 's1': 1, 's2': 0, 'flag': 'B', 'line': 6, 'row': 20, 'column': 5, 'type': 10, 'id': 'B-6-5-20', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 47}, {'x': 1870.54688, 'y': 13.8274679, 'z': 48.6279373, 's1': 1, 's2': 0, 'flag': 'A', 'line': 13, 'row': 18, 'column': 4, 'type': 15, 'id': 'A-13-4-18', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 48}, {'x': 1899.98157, 'y': 19.2024975, 'z': 50.3567772, 's1': 1, 's2': 0, 'flag': 'B', 'line': 14, 'row': 25, 'column': 50, 'type': 15, 'id': 'B-14-50-25', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 49}, {'x': 1877.58582, 'y': 0.7738123, 'z': 36.62432, 's1': 1, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 15, 'type': 15, 'id': 'A-5-15-1', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 50}, {'x': 1893.59387, 'y': 4.613105, 'z': 42.17527, 's1': 1, 's2': 0, 'flag': 'B', 'line': 8, 'row': 6, 'column': 40, 'type': 15, 'id': 'B-8-40-6', 'bidBatch': '2020年第一批', 'factory': '深圳科陆', 'num': 51}, {'x': 1885.90771, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 0, 'flag': 'A', 'line': 13, 'row': 3, 'column': 28, 'type': 15, 'id': 'A-13-28-3', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 52}, {'x': 1883.3446, 'y': 4.613105, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 6, 'column': 24, 'type': 15, 'id': 'A-9-24-6', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 53}, {'x': 1886.54578, 'y': 17.6667786, 'z': 48.6279373, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 23, 'column': 29, 'type': 10, 'id': 'A-13-29-23', 'bidBatch': '2019年第一批', 'factory': '杭州炬华', 'num': 54}, {'x': 1883.98486, 'y': 8.452438, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 11, 'column': 25, 'type': 10, 'id': 'A-9-25-11', 'bidBatch': '2019年第二批', 'factory': '杭州炬华', 'num': 55}, {'x': 1872.464, 'y': 5.380984, 'z': 42.17527, 's1': 0, 's2': 1, 'flag': 'B', 'line': 8, 'row': 7, 'column': 7, 'type': 10, 'id': 'B-8-7-7', 'bidBatch': '2020年第一批', 'factory': '宁夏隆基', 'num': 56}, {'x': 1871.82764, 'y': 3.84524536, 'z': 42.17527, 's1': 0, 's2': 1, 'flag': 'B', 'line': 8, 'row': 5, 'column': 6, 'type': 10, 'id': 'B-8-6-5', 'bidBatch': '2021年第一批', 'factory': '杭州炬华', 'num': 57}, {'x': 1883.98486, 'y': 17.6667786, 'z': 47.6289978, 's1': 0, 's2': 1, 'flag': 'B', 'line': 12, 'row': 23, 'column': 25, 'type': 10, 'id': 'B-12-25-23', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 58}, {'x': 1876.30713, 'y': 6.14884233, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 8, 'column': 13, 'type': 10, 'id': 'B-6-13-8', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 59}, {'x': 1889.10876, 'y': 15.3631821, 'z': 45.8976822, 's1': 0, 's2': 1, 'flag': 'A', 'line': 11, 'row': 20, 'column': 33, 'type': 10, 'id': 'A-11-33-20', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 60}, {'x': 1871.18518, 'y': 15.3632011, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 20, 'column': 5, 'type': 10, 'id': 'B-6-5-20', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 61}, {'x': 1870.54688, 'y': 13.8274679, 'z': 48.6279373, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 18, 'column': 4, 'type': 15, 'id': 'A-13-4-18', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 62}, {'x': 1899.98157, 'y': 19.2024975, 'z': 50.3567772, 's1': 0, 's2': 1, 'flag': 'B', 'line': 14, 'row': 25, 'column': 50, 'type': 15, 'id': 'B-14-50-25', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 63}, {'x': 1877.58582, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 1, 'flag': 'A', 'line': 5, 'row': 1, 'column': 15, 'type': 15, 'id': 'A-5-15-1', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 64}, {'x': 1893.59387, 'y': 4.613105, 'z': 42.17527, 's1': 0, 's2': 1, 'flag': 'B', 'line': 8, 'row': 6, 'column': 40, 'type': 15, 'id': 'B-8-40-6', 'bidBatch': '2020年第一批', 'factory': '深圳科陆', 'num': 65}, {'x': 1885.90771, 'y': 2.3095293, 'z': 48.62794, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 28, 'type': 15, 'id': 'A-13-28-3', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 66}, {'x': 1883.3446, 'y': 4.613105, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 6, 'column': 24, 'type': 15, 'id': 'A-9-24-6', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 67}, {'x': 1871.82764, 'y': 6.14884233, 'z': 38.3443832, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 8, 'column': 6, 'type': 10, 'id': 'B-6-6-8', 'bidBatch': '2021年第一批', 'factory': '宁夏隆基', 'num': 68}, {'x': 1873.74841, 'y': 10.7560148, 'z': 42.17527, 's1': 1, 's2': 1, 'flag': 'B', 'line': 8, 'row': 14, 'column': 9, 'type': 10, 'id': 'B-8-9-14', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 69}, {'x': 1887.82837, 'y': 7.68457127, 'z': 50.35678, 's1': 1, 's2': 1, 'flag': 'B', 'line': 14, 'row': 10, 'column': 31, 'type': 10, 'id': 'B-14-31-10', 'bidBatch': '2019年第二批', 'factory': '深圳科陆', 'num': 70}, {'x': 1888.46655, 'y': 13.8274679, 'z': 42.17527, 's1': 1, 's2': 1, 'flag': 'B', 'line': 8, 'row': 18, 'column': 32, 'type': 11, 'id': 'B-8-32-18', 'bidBatch': '2020年第一批', 'factory': '深圳科陆', 'num': 71}, {'x': 1889.743, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 34, 'type': 11, 'id': 'A-13-34-3', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 72}, {'x': 1896.7876, 'y': 6.916702, 'z': 50.35678, 's1': 1, 's2': 1, 'flag': 'B', 'line': 14, 'row': 9, 'column': 45, 'type': 11, 'id': 'B-14-45-9', 'bidBatch': '2016年第一批', 'factory': '深圳科陆', 'num': 73}, {'x': 1899.34912, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 49, 'type': 11, 'id': 'A-13-49-3', 'bidBatch': '2019年第二批', 'factory': '杭州炬华', 'num': 74}, {'x': 1874.38452, 'y': 9.220296, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 12, 'column': 10, 'type': 11, 'id': 'A-9-10-12', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 75}, {'x': 1875.66882, 'y': 16.1310234, 'z': 47.6289978, 's1': 1, 's2': 1, 'flag': 'B', 'line': 12, 'row': 21, 'column': 12, 'type': 11, 'id': 'B-12-12-21', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 76}, {'x': 1896.7876, 'y': 1.54167175, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 2, 'column': 45, 'type': 13, 'id': 'A-5-45-2', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 77}, {'x': 1871.82764, 'y': 1.5416708, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 2, 'column': 6, 'type': 13, 'id': 'A-9-6-2', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 78}, {'x': 1900.63, 'y': 1.54167175, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 2, 'column': 51, 'type': 13, 'id': 'A-13-51-2', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 79}, {'x': 1901.27039, 'y': 1.54167175, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 2, 'column': 52, 'type': 13, 'id': 'A-11-52-2', 'bidBatch': '2021年第一批', 'factory': '苏源杰瑞', 'num': 80}, {'x': 1873.74841, 'y': 0.7738123, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 1, 'column': 9, 'type': 13, 'id': 'A-5-9-1', 'bidBatch': '2019年第一批', 'factory': '深圳科陆', 'num': 81}, {'x': 1880.14307, 'y': 4.613105, 'z': 53.2860031, 's1': 1, 's2': 1, 'flag': 'B', 'line': 16, 'row': 6, 'column': 19, 'type': 15, 'id': 'B-16-19-6', 'bidBatch': '2021年第一批', 'factory': '宁波三星', 'num': 82}, {'x': 1882.71045, 'y': 4.613105, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 6, 'column': 23, 'type': 15, 'id': 'A-11-23-6', 'bidBatch': '2020年第一批', 'factory': '苏源杰瑞', 'num': 83}, {'x': 1877.58582, 'y': 11.5238724, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 15, 'column': 15, 'type': 15, 'id': 'A-5-15-15', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 84}]
    #CargoNow = CargoNow_sql.getGoodsLocationInfoVice()
    R = 39
    S = 14
    H = 14
    C = 17
    LineTimeList=[ 31.84, 32.69, 34.55, 35.41, 37.29, 38.15, 40.02, 40.88, 42.78, 44.70, 46.58 ]
    LisCross = [[[1,3,47.11],[3,4,17.78]],[[2,3,5.17],[3,4,17.78]]] #程天宇计算
    #各种类型的上货数量  
    LisGoodsNum = [{'10':8,'11':6,'13':6,'15':7,'16':12}]

    graph_of_spots = [
        [1, 10, 9, 2.5],
        [1, 11, 9, 2.1],
        [2, 9, 5, 2.3],
        [3, 4, 2, 2.4],
        [3, 5, 2, 1.5],
        [3, 6, 2, 1.4],
        [4, 2, 1, 2.5],
        [6, 1, 3, 3],
        [7, 3, 8, 3.4],
        [7, 3, 7, 3.1]
    ]

    fold_id = 1  # 叠箱机的 id
    global LisInspect
    global LisReturnTime
    global inspectIndex #已读送检数量
    global returnIndex  #已读回库数量
    global LisEnterTime #入库资产到达对应入库口的时间
    global DdjEnterXYZ
    global DdjOutXYZ
    global DdjInspectXYZ
    global InspectTypeFloorNum
    global ReadInspectTypeNum
    global DirReturnXYZ
    global rrr#每个堆垛机对应的line，二维list
    global ans#所有line编号,一维set
    global r#所有入库的编号,一维set
    global dr#每个入库编号对应的line编号,一维dict3
    global lineToDdj
    global idToL
    global LisDdjTime
    lineToDdj={};
    idToL={};
    # global LisupLoadTimeLis #上货点到叠箱机的时间序列
    dr = {}
    r=set()
    ans = set();
    rrr=[];

    LisInspect = [{'2':[11,17,13]},{'3':[10]},{'4':[10,14]},{'5':[11,11]}]#json 文件中获得
    LisReturnTime = []
    LisEnterTime = []
    inspectIndex = 0
    returnIndex = 0
    DdjEnterXYZ = []  #[[[ddj1_x1.ddj1_y1,ddj1_z1],[...]],[[ddj2_x1,...],[....]],...[]]
    DdjOutXYZ = []  
    DirReturnXYZ = {}  
    DdjInspectXYZ = []   #[[二楼[堆垛机序号[堆垛机坐标]],[]]]
    InspectTypeFloorNum = []
    ReadInspectTypeNum = []
    LisDdjTime = []
def GetDdjDataXYZ(DdjData):
    global DdjEnterXYZ
    global DdjOutXYZ
    global DdjInspectXYZ
    #DdjData = ddjData_sql.getStacks()
    Lisfloor = []
    for i in range(len(DdjData)):
        for j in DdjData[i]:
            if '放货点' in j:
                Lisfloor.append(j)
    Lisfloor = DelList(Lisfloor)
    inspectFloorNum = len(Lisfloor) - 2
    for i in range(inspectFloorNum):
        DdjInspectXYZ.append([])
    for i in range (len(DdjData)):
        for j in DdjData[i]:
            if '一楼取放货点' in j:
                DdjEnterXYZ.append(DdjData[i].get('%s'%(j)))
            if '一楼出库放货点' in j:
                DdjOutXYZ.append(DdjData[i].get('%s'%(j)))
            if '二楼取放货点' in j:
                DdjInspectXYZ[0].append(DdjData[i].get('%s'%(j)))
            if '三楼取放货点' in j:
                DdjInspectXYZ[1].append(DdjData[i].get('%s'%(j)))
            if '四楼取放货点' in j:
                DdjInspectXYZ[2].append(DdjData[i].get('%s'%(j)))
            if '五楼取放货点' in j:
                DdjInspectXYZ[3].append(DdjData[i].get('%s'%(j)))
                

def Fitness(LisCode,DdjData):
    GetDdjDataXYZ(DdjData)
    global LisDdjTime 
    LisDdjCode = getLisDdjCode(LisCode) #按照堆垛机区分
    GetS_H(LisDdjCode)
    Read(LisDdjCode)
    LisDdjTime = sorted(LisDdjTime, reverse=True)
    return LisDdjTime[0]

def enSimpleCode(LisCode:list,DdjData):
    initCode()
    global LisEnterTime
    if(type(LisCode) == list and type(LisCode[0]) == int and type(LisCode[-1]) == int):
        #print("yes!")
        LisEnterTime = cal(LisCode,5) #叠箱机到堆垛机入库口
        fitness = round(Fitness(LisCode,DdjData),3)
        return fitness
    else:
        print("LisCode Error!")
        return 0


LisCode = [76, 2, 9, 14, 39, 22, 82, 60, 70, 58, 4, 59, 30, 74, 20, 80, 8, 71, 54, 48, 83, 65, 51, 75, 12, 36, 66, 34, 28, 73, 56, 13, 64, 68, 55, 24, 11, 45, 49, 26, 79, 46, 33, 18, 15, 10, 5, 27, 72, 31, 29, 23, 52, 38, 35, 6, 41, 25, 16, 69, 43, 19, 44, 1, 42, 40, 17, 84, 62, 32, 67, 61, 53, 63, 7, 50, 78, 37, 21, 77, 3, 57, 81, 47]
#print(len(LisCode))
DdjData = ddjData_sql.getStacks()
print(enSimpleCode(LisCode,DdjData))
print(enSimpleCode(LisCode,DdjData))
#print(cal(LisCode,5))

# print(len(CargoNow_sql.getGoodsLocationInfoVice()))
#print(ddjData_sql.getStacks()[0])