# 准备工作
## conda安装
前往anconda官网，下载 [anconda3](https://www.anaconda.com/download/ "anconda3下载")\
或者 *Windows* 使用 **scoop** 安装
```shell
scoop install conda
```
## 克隆项目到本地
```shell
git clone https://github.com/GentsunCheng/FindLicense.git
```
# 环境配置
## conda环境配置
进入到克隆的项目目录下
```shell
cd FindLicense
```
创建conda隔离环境
```shell
conda env create -f environment.yml
```
进入conda环境
```shell
conda activate FindLicense
```
安装所需的python库
```shell
pip install -r requirements.txt
```
# 运行程序(二选一)
如果你是在纯命令行，则在进入conda环境后，直接使用
```shell
python src/app.py
```
若使用的PyCharm编译器，则直接 **Shift+F10** 或单击运行按钮启动程序