import math

def calculate_direction_angle(point1, point2):
    # 1. 方向ベクトルを計算する
    direction_vector = (point2[0] - point1[0], point2[1] - point1[1], point2[2] - point1[2])
    
    # 2. 各成分の角度を計算する
    x_angle = math.atan2(direction_vector[1], direction_vector[0])
    y_angle = math.atan2(direction_vector[2], math.sqrt(direction_vector[0]**2 + direction_vector[1]**2))
    z_angle = math.atan2(math.sqrt(direction_vector[0]**2 + direction_vector[1]**2), direction_vector[2])
    
    # 3. 各軸周りの回転角度として解釈する
    x_rotation = math.degrees(x_angle)
    y_rotation = math.degrees(y_angle)
    z_rotation = math.degrees(z_angle)
    
    # 解析結果を返す
    return (x_rotation, y_rotation, z_rotation)

print("Result:",calculate_direction_angle([0,0,0],[1,1,1]))