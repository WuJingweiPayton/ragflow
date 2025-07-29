# 登录页面背景图片更换指南

## 📍 背景图片位置

登录页面右侧的背景图片在以下文件中定义：

- **文件路径**: `web/src/pages/login/index.less`
- **CSS 类**: `.loginRight::before`
- **当前图片**: `web/src/assets/svg/login-background.svg`

## 🔄 更换方法

### 方法1：直接替换文件（推荐）

```bash
# 1. 备份原文件
cp web/src/assets/svg/login-background.svg web/src/assets/svg/login-background.svg.backup

# 2. 替换为新图片（保持相同文件名）
cp your-new-background.svg web/src/assets/svg/login-background.svg
```

### 方法2：修改 CSS 路径

在 `web/src/pages/login/index.less` 文件中修改：

```less
.loginRight {
  &::before {
    /* 将这一行改为你的新图片路径 */
    background-image: url("@/assets/svg/your-new-background.svg");
  }
}
```

### 方法3：使用其他格式图片

1. 将图片文件放入 `web/src/assets/images/` 目录
2. 修改 CSS 路径：

```less
/* 使用 JPG 图片 */
background-image: url("@/assets/images/login-background.jpg");

/* 使用 PNG 图片 */
background-image: url("@/assets/images/login-background.png");
```

### 方法4：使用在线图片

```less
background-image: url("https://example.com/your-background.jpg");
```

## 🎨 样式调整选项

### 背景尺寸 (background-size)

```less
background-size: cover; /* 覆盖整个容器（当前使用） */
background-size: contain; /* 完整显示图片 */
background-size: 100% 100%; /* 拉伸填充 */
```

### 背景位置 (background-position)

```less
background-position: center; /* 居中显示（当前使用） */
background-position: top center; /* 顶部居中 */
background-position: bottom center; /* 底部居中 */
```

### 混合模式 (background-blend-mode)

```less
background-blend-mode: multiply; /* 正片叠底（当前使用） */
background-blend-mode: overlay; /* 叠加效果 */
background-blend-mode: soft-light; /* 柔光效果 */
background-blend-mode: screen; /* 滤色效果 */
```

### 滤镜效果 (filter)

```less
filter: blur(3px); /* 模糊效果（当前使用） */
filter: blur(0px); /* 无模糊 */
filter: brightness(1.2); /* 增加亮度 */
filter: contrast(1.2); /* 增加对比度 */
filter: saturate(1.5); /* 增加饱和度 */
```

## 📝 注意事项

1. **图片格式**: 推荐使用 SVG、JPG 或 PNG 格式
2. **图片大小**: 建议图片文件大小控制在 5MB 以内
3. **图片尺寸**: 建议使用高分辨率图片（至少 1920x1080）
4. **文件路径**: 确保图片文件路径正确
5. **缓存问题**: 更换图片后可能需要清除浏览器缓存

## 🔧 测试步骤

1. 更换图片文件或修改 CSS
2. 重新编译项目：`npm run build`
3. 启动开发服务器：`npm run dev`
4. 访问 `/login` 页面查看效果
5. 清除浏览器缓存（Ctrl+F5）确保看到新图片

## 📁 文件结构

```
web/src/
├── assets/
│   ├── svg/
│   │   └── login-background.svg    # 当前背景图片
│   └── images/                     # 新建的图片目录
│       └── login-background.jpg    # 可选的 JPG 图片
└── pages/
    └── login/
        └── index.less              # 样式文件
```
