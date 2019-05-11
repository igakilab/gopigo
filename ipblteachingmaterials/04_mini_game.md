# Overview of the Real World Game Programming Shooting Competition Rule for minigame (2nd day)
- Each team has 2 robots. One is Shooter, another is Guard.
- Shooter shoots photos of 3 targets many times with picamera.
  - Each field has 3 targets, yellow, green and blue.
- Guard protects them not to be shot from Shooter.
- In a mini game, let's play an in-team match with a Shooter / Guard robot

## Field
- The following figure represents the competition field (1.5m * 2.5m).
- First, shooter and guard are located at each start position.

<a href="https://sites.google.com/site/ipbloit/private/2019/04/field.jpg"><img src="https://sites.google.com/site/ipbloit/private/2019/04/field.jpg" border="0" width="800"></a>

## Rule
- You should set a value of the gopigo's speed between **0~500**.
  - Note:Though you can set any positive value as the speed value, too big value may damage the gopigo.
- Shooter and guard robot should not cross the center line.
  - If a robot invade the opponent area, referee moves the robot to the starting point.
- Each image captured by a shooter is checked by our following judge program.
  - [judge program for minigame](http://bit.ly/judge_mini)
  - Judge rule is as follows. If a colored target area in a captured image is more than 5 % of 200 px * 150 px area, you will get a point.

<a href="https://sites.google.com/site/ipbloit/private/2019/04/judge.jpg"><img src="https://sites.google.com/site/ipbloit/private/2019/04/judge.jpg" border="0" width="500"></a>

- Shooter has to shoot photos of different colored targets sequentially, as follows.

<a href="https://sites.google.com/site/ipbloit/private/2019/04/judge2.jpg"><img src="https://sites.google.com/site/ipbloit/private/2019/04/judge2.jpg" border="0" width="500"></a>

- yellow(point 1), green(point 2), blue(point 3), blue(point 3), green(point 4), yellow(point 5), yellow(point 5)...
  - That is, Shooter cannot gain a point if the shooter shoots photos of same colored target sequentially.
- If more than **20 (minigame) or 200 (final competition)** images are captured by a shooter, the judge program **automatically deletes them**.

# Flow of Mini Game (Robots are controlled manually)
- Let's controls 2 robots (Shooter/Guard) **manually** with keyboard through wifi.
  - A Shooter robot shoots targets and a Guard robot prevents targets from being shot by the shooter robot.

## Steps
- **First**, locate each robot at each start position.
- Referee starts the judge program in the shooter's raspbian.
  - Referee downloads the judge program ``wget http://bit.ly/judge_mini -O ipbl_judge_minigame.py`` at the shooter's program (gopigo-python program) directory.
  - **Note**
    - the gopigo-python program and the ipbl_judge...py should be located at the same directory.
    - Images captured by the gopigo-python(Shooter) program should be also saved at the directory.
  - Referee also downloads a html file to show the result ``sudo wget http://bit.ly/scorehtml -O score.html -P /var/www/html/``
  - Referee checks whether no image exists to be judged in the shooter's raspbian.
  - Execute `sudo python ipbl_judge_minigame.py 30 75 105 TeamOraora`
    - 30 75 105 means default hue value of yellow, green and blue, respectively. In actual minigame, each team indicates each base h value for judge program.
    - TeamOraora means a team name which does not include space character.
- Please offers wifi ip address of the Shooter robot.
  - Referee displays score.txt on the browser based on the wifi ip address.
    - `ipbl_judge_minigame.py` shows the shooter's score in the following url.
    - `http://shooter's wireless IP/score.html`

- In accordance with the referee's signal ("Ready Go"), each team starts a gopigo-python program to move each robot and save target images by keyboard control.
- Referee may indicate to stop a robot and return it to the start position based on the following condition. 
  - A robot invades the opponent area.
  - A robot goes out from the filed.
- A game will end after 10 miniutes has elapsed.
