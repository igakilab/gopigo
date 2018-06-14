# Overview of the Real World Game Programming Shooting Competition Rule
- Each team has 2 robots. One is Shooter, another is Guard.
- Shooter shoots 3 targets many times.
  - Each field has 3 targets, yellow, green and blue.
- Guard protect them not to be shot from Shooter.

## Field
- The following figure represents the competition field (1.5m * 2.5m).
- First, shooter and guard are located at each start position.

<a href="https://sites.google.com/site/ipbloit/2018/04/field.jpg"><img src="https://sites.google.com/site/ipbloit/2018/04/field.jpg" border="0" width="800"></a>

- Each team has each field.
- In minigame and final competition, **every shooter uses their own field, and every guard moves to the other team's field**.
  - Team of the guard can ask the value of h_base for each color to the shooter's team, in the field.

## Rule
- Shooter and guard robot should not cross the center line.
  - If a robot invade the opponent area, referee moves the robot to the starting point.
- Each image captured by a shooter is checked by our following judge program.
  - judge program for minigame:
  - judge program for final competition:

- Shooter must shoot different colored targets sequentially, as follows.
  - yellow(point 1), blue(point 2), blue(point 2), green(point 3), yellow(point 4), yellow(point 4), green(point 5)...
    - That is, Shooter cannot gain a point if the shooter shoots same colored target sequentially.
- If more 20 (minigame) or 200 (final competition) images are captured by a shooter, the judge program automatically deletes them. 

# Flow of Mini Game (Robots are controlled manually)
- Every team controls 2 robots (Shooter/Guard) **manually** with keyboard through wifi.
  - Shooter robots shoot targets and Guard robots protect it .

## Steps
- **First**, both teams locate each robot at each start position.
- Referee starts the judge program in the shooter's raspbian.
  - Referee checks whether no image exists to be judged in the shooter's raspbian.
  - Execute `sudo python ipbl_judge_minigame.py 60 150 80`
    - 60 150 80 means base h value of yellow, green and blue, respectively. In actual minigame, each team indicates each base h value for judge program.
  - yello,green,blue indicates each H_base value, respectively. Actual h_base value is offered by each shooter's team.
- In accordance with the referee's signal ("Ready Go"), each team starts a gopigo-python program to move each robot and save target images by keyboard.
  - **Note**
    - the gopigo-python program and the ipbl_judge...py should be located at same directory.
    - Images captured by the gopigo-python program are also saved at the directory.
- Every team should follow the instructions of the referee. 
- A robot should not invade the opponent area.
- A robot should not go out from the filed.
- A game will end after 10 miniutes has elapsed.
- `ipbl_judge_minigame.py` shows the shooter's score on web.
  - `http://shooter's wireless IP/score.txt`

# Flow of Final Competition (Robots move autonomously)
- Shooter and Guard robots achieve their objectives **autonomously**.

## Steps
- **First**, both teams Locate each robot at each start position.
- Referee starts the judge program in the shooter's raspbian.
  - Referee checks whether no image exists to be judged in the shooter's raspbian.
  - Execute `sudo python ipbl_judge_final.py 60 150 80`
    - 60 150 80 means base h value of yellow, green and blue, respectively. In actual minigame, each team indicates each base h value for judge program.
  - yello,green,blue indicates each H_base value, respectively. Actual h_base value is offered by each shooter's team.
- In accordance with the referee's signal ("Ready Go"), each team member starts a gopigo-python program to move each robot and save target images autonomously.
  - **Note**
    - the gopigo-python program and the ipbl_judge...py should be located at same directory.
    - Images captured by the gopigo-python program are also saved at the directory.
- Referee may indicate to stop a robot and return it to the start position based on the following condition. 
  - A robot invades the opponent area.
  - A robot stops for about 1 minute.
  - A robot goes out from the filed.
- Even if a Guard robot is stopped by the referee, shooter robot should not be stopped, and vice versa.
- A game will end after 10 miniutes has elapsed.
- `ipbl_judge_final.py` shows the shooter's score.
  - `http://shooter's wireless IP/score.txt`

## Award of Final Competition
- `#` of Win
- (MVS)Most Valuable Shooter
  - Shooter with the highest average score
- (MVG)Most Valuable Guard
  - Guard with the lowest average score
