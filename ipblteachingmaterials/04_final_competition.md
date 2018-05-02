# Final Competition Rule

## Overview of the Real World Game Programming Shooting Competition Rule
- Each team has 2 robots. One is Shooter, another is Guard.
- Shooterはターゲットを撮影しなければならない
  - Each field has 3 targets, yellow, green and blue.
- GuardはShooterによる撮影を防がなければならない

## Field
- The following figure represents the competition field (1.5m * 2.5m).
- First, shooter and guard are located at each start position.

<a href="https://sites.google.com/site/ipbloit/private/2018/04/field.jpg"><img src="https://sites.google.com/site/ipbloit/private/2018/04/field.jpg" border="0" width="800"></a>

## Rule
- Shooter and guard robot should not cross the center line.
  - If a robot invade the opponent area, referee indicate to stop the robot.
- Each image captured by a shooter must satisfy the following conditions.
  - The area of the target is over 10000px.
  - The center.x of the target in the image is between 200px and 400px.
- 上記の条件を満たす画像群を対象にスコアを計算する．計算のためのアルゴリズムは以下のとおり．
  - 画像群のうち，ターゲットが適切に撮影されている画像群を抽出する．
    - すべての画像はjpg形式で保存されなければならない
  - 抽出した画像群を撮影時刻順にソートする
  - 各画像のターゲットカラーを特定し，撮影時刻順に並べる
  - 連続して異なるカラーのターゲットが撮影されていると，ポイントを追加する
    - ex. yellow,green,blue,blue,green -> 3P
  - ターゲットカラーが特定されたすべての画像を対象にスコアを計算する

## Game Flow
- Locate each robot at each start position respectively.
- Referee starts the evaluation program in the shooter's raspbian.
  - Referee checks whether no image exists to be evaluated in the shooter's raspbian.
  - `python check_score.pyc yellow=60 green=150 blue=80`
  - yello,green,blue indicates each H_base value, respectively. Actual h_base value is indicated by each shooter's team.
- In accordance with the referee's signal ("Ready Go"), each team member activates each robot by pressing any key.
- Referee may indicate to stop a robot and return it to the start position based on the following condition. 
  - A robot invades the opponent area.
  - A robot stops for about 1 minute.
  - A robot goes out from the filed.
- Even if a Guard robot is stopped by the referee, shooter robot should not be stopped.
- A game will end after 10 miniutes has elapsed.
- `check_score.pyc` shows the shooter's score.

## Award
- (MVS)Most Valuable Shooter
- (MVG)Most Valuable Guard
