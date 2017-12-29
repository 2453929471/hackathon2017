## Introduction

In Object-oriented programming, classes can grow too big with many vaiables and functtions, so 
we need code refactoring to improve code quality.

This tool can:
* analyses simple source codes and gives advices about how to separate a big class 
   into several small classes. 
* provides the visualizaion of class structure.


## Requirements:

* python3.5+
* igraph  (optional)
* plotly  (optional)
* pygame  (optional)
    
    
## Usage：

    python3 main.py code.h code.cpp             ----generate txt result
    python3 main.py -v --csv code.h code.cpp    ----generate csv used for workstation
    python3 main.py -v --ploty code.h code.cpp  ----generate 3D result
    python3 main.py -v --pygame code.h code.cpp ----generage 2D result
    
ATTENTION: .h and .cpp files have to be in the same directory of main.py

* 3D example:

<div>
    <a href="https://plot.ly/~mgao/6/?share_key=y7DKcnHtnLWmsMhd2Wxued" target="_blank" title="base" style="display: block; text-align: center;"><img src="https://plot.ly/~mgao/6.png?share_key=y7DKcnHtnLWmsMhd2Wxued" alt="base" style="max-width: 100%;width: 1100px;"  width="1100" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
    <script data-plotly="mgao:6" sharekey-plotly="y7DKcnHtnLWmsMhd2Wxued" src="https://plot.ly/embed.js" async></script>
</div>
