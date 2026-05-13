# 一款融合了类幸存者与营地建造的小游戏

## 🍔 游戏逻辑

- 在类幸存者模式下的肉鸽战斗中**收集材料**  
- 通过收集的材料在营地中**升级建筑、制造装备**  
- 获得更强的加成进入下一场战斗  

## ✨ 主要特性

- **🌍 无缝生成地形 + 六种生态群落**   
  基于双维度 Perlin 噪声实时生成 **热带雨林、沙漠、温带森林、草原、苔原、冰川** 六种生物群落  
  通过种子使每局生成的地图不同

- **🗺️ 生成动态小地图**   
  小地图使用色块代表六种地形，原点代表角色当前位置  
  仅显示玩家已探索区域，未探索区域保持黑色（迷雾模式）      

- **⚔️ 类幸存者战斗模式（肉鸽）**   
  自动旋转武器击杀怪物、自动吸收经验升级、升级时三选一词条强化  
  击杀敌人掉落材料，靠近自动吸取  

- **🏕️ 营地建设 + 工作台合成**   
  战斗获得的材料用于升级 **铁匠铺、训练场、魔法塔、仓库** ，永久提升角色属性   
  营地中自由移动，可与建筑交互升级，与工作台交互合成道具  

- **🎒 装备 + 消耗品系统**   
  消耗材料可合成并使用装备或道具，如：  
   - **铁镐**（增加材料掉落）  
   - **生命药水**（永久提升最大生命）等  
  装备可在营地界面自由穿戴，效果带入下一次战斗  

- **🔧 地图资源交互**  
  - 采集地图上的树木、矿石等装饰物，获得不同材料   
  - 按 `U` 打开背包查看材料与装备，使用消耗品  
  - 按 `I` 打开装备界面，穿戴/卸下装备

- **💾 支持数据持久化**  
  材料库存、建筑等级、装备列表均保存至json文件，死亡后材料归零但营地库存累加

## 🌳运行环境
- python 3.12  
- pygame 2.6.1
- opensimplex 0.4.5.1

## 🧰 项目结构
PygameProject/  
├── main.py                 # 游戏入口，场景切换  
├── settings.py             # 全局配置（地图、人物、武器设置，地形参数等）  
├── formula.py              # 装备配置（合成列表等）  
├── game.py                 # 战斗场景主逻辑  
├── camp.py                 # 营地场景  
├── entities/               # 玩家、敌人、武器、装饰物、材料等的实体类  
├── managers/               # 输入、碰撞、经验、材料、装备、存档等的控制类  
├── ui/                     # 背包、合成台、装备界面等 UI  
├── world/                  # 地图生成、相机、小地图  
├── assets/                 # 贴图资源  
└── data/                   # 存档文件  

## 🏜️ 游戏截图  
![image](https://github.com/Crychrip/PygameProject/blob/main/assets/display/%E5%8D%87%E7%BA%A7.png)  
![image](https://github.com/Crychrip/PygameProject/blob/main/assets/display/%E5%90%88%E6%88%90.png)  
![image](https://github.com/Crychrip/PygameProject/blob/main/assets/display/%E5%9C%BA%E6%99%AF1.png)  
![image](https://github.com/Crychrip/PygameProject/blob/main/assets/display/%E5%9C%BA%E6%99%AF2.png)  
![image](https://github.com/Crychrip/PygameProject/blob/main/assets/display/%E5%9C%BA%E6%99%AF3.png)  
![image](https://github.com/Crychrip/PygameProject/blob/main/assets/display/%E8%83%8C%E5%8C%85.png)  
![image](https://github.com/Crychrip/PygameProject/blob/main/assets/display/%E8%90%A5%E5%9C%B0.png)  
![image](https://github.com/Crychrip/PygameProject/blob/main/assets/display/%E8%A3%85%E5%A4%87.png)  
