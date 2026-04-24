# manimgl-imcommit
Manim(3Blue1Brown) Korean channel <br /> 

## raenim
manim 기반 utility tool  
[링크](https://github.com/CodingVillainKor/raenim)에서 설치하신 후 아래와 같이 import해서 사용하실 수 있습니다
```python
from raenimgl import *

# Scene2D, Scene3D, PythonCode, MINT, ...
``` 

## How to start
### 내 프로젝트 시작하기:
```bash
$ uv init_project.py --name my_manim
```


### Manim impl. 기본기:
1. 클래스가 하나의 영상입니다
2. `manim main.py <class_name>` 실행 시 <class_name>.construct()를 실행합니다
3. 생성된 영상은 `videos/`에 저장됩니다

## turboquant1
Turboquant1: What is quantization?
[[YouTube link]](https://youtu.be/WH6sNfPzEDk) <br />
```bash
$ cd src/turboquant1
$ uv run manimgl main.py
```