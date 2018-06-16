# Overview of the Real World Game Programming Shooting Competition Rule for minigame (2nd day) and final competition (final day)
- Each team has 2 robots. One is Shooter, another is Guard.
- Shooter shoots 3 targets many times.
  - Each field has 3 targets, yellow, green and blue.
- Guard protect them not to be shot from Shooter.

## Field
- The following figure represents the competition field (1.5m * 2.5m).
- First, shooter and guard are located at each start position.

<a href="https://sites.google.com/site/ipbloit/2018/04/field.jpg"><img src="https://sites.google.com/site/ipbloit/2018/04/field.jpg" border="0" width="500"></a>

- Each team has each field.
- In minigame and final competition, **every shooter uses their own field, and every guard moves to the other team's field**.
  - Team of the guard can ask the value of h_base for each color to the shooter's team, in the field.

## Rule
- Shooter and guard robot should not cross the center line.
  - If a robot invade the opponent area, referee moves the robot to the starting point.
- Each image captured by a shooter is checked by our following judge program.
  - [judge program for minigame](http://bit.ly/judge_mini)
  - [judge program for final competition](http://bit.ly/judge_final)
  - Judge rule is as follows. If a colored target in a captured image is more than 5 % of 200 px * 150 px area, you will get a point.

<a href="https://sites.google.com/site/ipbloit/2018/04/judge.jpg"><img src="https://sites.google.com/site/ipbloit/2018/04/judge.jpg" border="0" width="500"></a>

- Shooter must shoot different colored targets sequentially, as follows.

<a href="https://sites.google.com/site/ipbloit/2018/04/judge2.jpg"><img src="https://sites.google.com/site/ipbloit/2018/04/judge2.jpg" border="0" width="500"></a>

- yellow(point 1), green(point 2), blue(point 3), blue(point 3), green(point 4), yellow(point 5), yellow(point 5)...
  - That is, Shooter cannot gain a point if the shooter shoots same colored target sequentially.
- If more **20 (minigame) or 200 (final competition)** images are captured by a shooter, the judge program **automatically deletes them**.

# Flow of Mini Game (Robots are controlled manually)(2nd day 11:00 AM)
- Every team controls 2 robots (Shooter/Guard) **manually** with keyboard through wifi.
  - Shooter robots shoot targets and Guard robots protect it.

## Steps
- **First**, both teams locate each robot at each start position.
- Referee starts the judge program in the shooter's raspbian.
  - Referee downloads the judge program ``wget http://bit.ly/judge_mini -O ipbl_judge_minigame.py`` at the shooter's program (gopigo-python program) directory.
  - **Note**
    - the gopigo-python program and the ipbl_judge...py should be located at same directory.
    - Images captured by the gopigo-python program are also saved at the directory.
  - Referee checks whether no image exists to be judged in the shooter's raspbian.
  - Execute `sudo python ipbl_judge_minigame.py 30 75 105 TeamOraora`
    - 30 75 105 means default hue value of yellow, green and blue, respectively. In actual minigame, each team indicates each base h value for judge program.
    - TeamOraora means a team name which does not include space character.
- The team of Shooter offers wifi ip address of the Shooter.
  - Referee displays score.txt on the browser based on the wifi ip address.
    - `ipbl_judge_minigame.py` shows the shooter's score in the following url.
    - `http://shooter's wireless IP/score.txt`

- In accordance with the referee's signal ("Ready Go"), each team starts a gopigo-python program to move each robot and save target images by keyboard control.
- Referee may indicate to stop a robot and return it to the start position based on the following condition. 
  - A robot invades the opponent area.
  - A robot goes out from the filed.
- A game will end after 10 miniutes has elapsed.

# Flow of Final Competition (Robots move autonomously)(Final Day AM)
- Shooter and Guard robots achieve their objectives **autonomously**.

## Steps
- **First**, both teams Locate each robot at each start position.
- Referee starts the judge program in the shooter's raspbian.
  - Referee downloads the judge program ``wget http://bit.ly/judge_final -O ipbl_judge_final.py`` at the shooter's program (gopigo-python program) directory.
  - **Note**
    - the gopigo-python program and the ipbl_judge...py should be located at same directory.
    - Images captured by the gopigo-python program are also saved at the directory.
  - Referee checks whether no image exists to be judged in the shooter program's directory.
  - Execute `sudo python ipbl_judge_final.py 30 75 105 TeamDoraemon`
    - 30 75 105 means default hue value of yellow, green and blue, respectively. In actual final competition, each team indicates each base h value for judge program.
    - TeamDoraemon means a team name which does not include space character.
- The team of Shooter offers wifi ip address of the Shooter.
  - Referee displays score.txt on the browser based on the wifi ip address.
    - `ipbl_judge_final.py` shows the shooter's score in the following url.
    - `http://shooter's wireless IP/score.txt`

- In accordance with the referee's signal ("Ready Go"), each team member starts a gopigo-python program to move each robot and save target images autonomously.
- Referee may indicate to stop a robot and return it to the start position based on the following condition. 
  - A robot invades the opponent area.
  - A robot stops for about 1 minute.
  - A robot goes out from the filed.
- During the game, you can start and stop the gopigo-python program at any time though controlling the gopigo with keyboard directry is prohibited.
- A game will end after 10 miniutes has elapsed.

## Award of Final Competition
- `#` of Win
- (MVS)Most Valuable Shooter
  - Shooter with the highest average score
- (MVG)Most Valuable Guard
  - Guard with the lowest average score
