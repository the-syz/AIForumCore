# VSCode配置LaTeX笔记

## 1. 在VSCode中配置LaTeX

### 安装步骤

1. **安装VSCode** ：从官网下载并安装Visual Studio Code
2. **安装LaTeX发行版** ：推荐安装TeX Live或MiKTeX（完整安装）
3. **安装VSCode扩展** ：在VSCode中安装"LaTeX Workshop"扩展

### 配置步骤

根据[Rosetears教程](https://rosetears.cn/archives/73/)的方案，添加以下配置到VSCode的settings.json中（这里的不全，建议还是看人教程里的）：

```json
{
    "latex-workshop.latex.recipes": [
        {
            "name": "xelatex",
            "tools": ["xelatex"]
        },
        {
            "name": "xelatex -> bibtex -> xelatex*2",
            "tools": ["xelatex", "bibtex", "xelatex", "xelatex"]
        }
    ],
    "latex-workshop.latex.tools": [
        {
            "name": "xelatex",
            "command": "xelatex",
            "args": [
                "-synctex=1",
                "-interaction=nonstopmode",
                "-file-line-error",
                "%DOC%.tex"
            ]
        },
        {
            "name": "bibtex",
            "command": "bibtex",
            "args": ["%DOC%"]
        }
    ],
    "latex-workshop.view.pdf.viewer": "tab"
}
```

### 环境变量配置（解决where xelatex找不到的问题）

如果安装完成后在命令行中无法找到xelatex，可以手动添加路径：

1. **找到LaTeX安装目录** ：通常为C:\texlive\2025\bin（根据实际版本调整）
2. **添加到环境变量** ：

* 右键点击"此电脑" → "属性" → "高级系统设置" → "环境变量"
* 在"系统变量"中找到"Path"，点击"编辑"
* 添加LaTeX的bin目录路径（例如：C:\texlive\2025\bin）
* 保存并重启VSCode

### 环境变量配置（解决安装时卡在加载镜像界面的问题）

若在安装过程中卡在加载镜像界面，且确认网络连接正常后，可检查系统用户名是否为英文。

若用户名包含中文字符，请按以下步骤修改环境变量：1. 打开系统环境变量设置界面（右键“此电脑”→“属性”→“高级系统设置”→“环境变量”）。

1. 在“系统变量”中分别选中TEMP和TMP变量，点击“编辑”。
2. 将变量值修改为%SystemRoot%\TEMP。
3. 保存设置并重启系统，以确保修改生效。

---

## 2. 配置Zotero引用

### 安装Zotero与插件1.  **安装Zotero** ：从[Zotero官网](https://www.zotero.org/)下载并安装

1. **安装Better BibTeX插件** ：

* 打开Zotero → 点击"工具" → "插件"
* 点击右上角齿轮图标 → "Install Add-on From File..."
* 从[Better BibTeX发布页](https://github.com/retorquere/zotero-better-bibtex/releases)下载最新的.xpi文件并安装
* 重启Zotero
  （也可以从zotero中文社区安装）

### 在VSCode中安装Zotero Cite插件1. 打开VSCode

1. 点击扩展图标（侧边栏中的方块图标）
2. 搜索并安装"Zotero Cite"插件
3. 重启VSCode

---

## 3. 使用方法

### 基本使用流程1. 在VSCode中打开.tex文件

1. 打开侧边栏中的TeX图标（LaTeX Workshop扩展的图标）
2. 点击"查看 LaTeX PDF"可以实时预览PDF，实现边写边看的效果

### 使用Zotero插入引用1. 运行Zotero

1. 在VSCode中，将光标放在需要插入引用的位置
2. 按下Ctrl+Shift+P打开命令面板
3. 输入并选择"Zotero Cite: Add Citation for Pandoc/Zotero"
4. 从弹出的Zotero引用选择器中选择对应的引用

### 导出BibTeX文件1. 在命令面板输入并选择"Zotero Cite:Export Biblatex"

1. 保存为.bib文件（默认文件名：ref.bib）
2. 在LaTeX文档中使用\bibliography{ref}命令引用该文件

### 编译文档* 点击vscode中的编译按钮即可编译

通过以上配置，你可以在VSCode中高效地编写LaTeX文档，并方便地管理和插入参考文献。
