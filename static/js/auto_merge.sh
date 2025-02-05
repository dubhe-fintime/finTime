#!/bin/bash

# 병합할 브랜치 설정
TARGET_BRANCH="main"
SOURCE_BRANCH="develop"

# 리포지토리 클론
git clone https://github.com/qkrdudals/dobot.git
cd D:\python_project\dobot_server

# 브랜치 체크아웃
git checkout $TARGET_BRANCH
git pull origin $TARGET_BRANCH

# 병합 시도
git merge origin/$SOURCE_BRANCH

# 병합 성공 시 푸시
if [ $? -eq 0 ]; then
  git push origin $TARGET_BRANCH
else
  echo "Merge conflict occurred. Attempting to resolve automatically."

  # 충돌 파일 리스트 가져오기
  CONFLICT_FILES=$(git diff --name-only --diff-filter=U)

  # 충돌 파일을 특정 브랜치로 해결
  for FILE in $CONFLICT_FILES; do
    git checkout --theirs $FILE
    git add $FILE
  done

  # 충돌 해결 후 커밋 및 푸시
  git commit -m "Resolved merge conflict on $(date)"
  git push origin $TARGET_BRANCH

  echo "Conflicts resolved and changes pushed."
fi
