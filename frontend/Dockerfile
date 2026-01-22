FROM node:20-alpine

WORKDIR /app

# 安装 pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# 复制依赖文件
COPY package.json pnpm-lock.yaml ./

# 安装依赖
RUN pnpm install --frozen-lockfile

# 复制源代码
COPY . .

# 构建应用
RUN pnpm build

EXPOSE 15173

# 使用 pnpm preview 启动，保持与开发环境一致
CMD ["pnpm", "preview", "--host", "0.0.0.0", "--port", "15173"]
