# PDF 번역기

<h5 align="center">
  이 저장소는 OpenAI GPT를 사용해 PDF 파일을 원본 레이아웃을 유지한 채 번역하는 WebUI와 API 엔드포인트를 제공합니다.
</h5>

<p align="center">
  <img src="./assets/example.png" width=70%>
</p>

## 특징

- PDF 파일의 레이아웃을 최대한 유지하며 번역

- 번역 엔진:
   - 구글 번역
   - OpenAI (최고, 기본)

- 레이아웃 인식 엔진:
   - UniLM DiT

- OCR 엔진:
   - PaddleOCR

- 폰트 인식 엔진:
  - simple (TimesNewRoman)
  - nanum (NanumMyeongjo)

## 설치

1. **저장소 클론**

```bash
   git clone https://github.com/refracta/pdf-translator-korean.git
   cd pdf_translator
```

2. **config.yaml 수정 후 OpenAI API 키 입력**
type을 'openai'로 변경하고 `openai_api_key`에 키를 입력합니다.
변경하지 않을 경우 번역 엔진은 기본적으로 구글 번역을 사용합니다.

또한 `layout` 섹션의 `dpi` 값을 조정하여 PDF를 이미지로 변환할 때의 해상도를 변경할 수 있습니다. 기본값은 200입니다.


### 도커 설치

3. **Makefile을 이용해 도커 이미지 빌드**

```bash
   make build
```

4. **Makefile을 이용해 도커 컨테이너 실행**

```bash
   make run
```

### 가상 환경 설치

3. **가상 환경 생성 및 활성화**

필수 패키지:
- ffmpeg 등... 문제가 발생한다면 Dockerfile을 참고하세요.

```bash
python3 -m venv .
source bin/activate
```

4. **필수 패키지 설치**

```bash
pip3 install -r requirements.txt
pip3 install "git+https://github.com/facebookresearch/detectron2.git"
```

5. **모델 다운로드**

```bash
make get_models
```

6. **실행**

```bash
python3 server.py
```

## GUI 사용

브라우저로 접속합니다.

```bash
http://localhost:8765
```

## 요구 사항

- NVIDIA GPU **(현재는 NVIDIA GPU만 지원)**
- Docker

## 라이선스

**이 저장소는 상업적 사용을 허가하지 않습니다.**

이 저장소는 CC BY-NC 4.0 라이선스 하에 있습니다. 자세한 내용은 [LICENSE](./LICENSE.md)를 참고하세요.

## TODO

- [ ] 번역된 텍스트 하이라이트 기능
- [ ] M1 Mac 또는 CPU 지원
- [ ] 레이아웃 감지를 VGT로 전환
- [ ] 글꼴 감지 (종류/스타일/색상/크기/정렬)
- [ ] 목록 번역 지원
- [ ] 테이블 번역 지원
- [ ] 이미지 내 텍스트 번역 지원

## 참고

- 기반 프로젝트: https://github.com/discus0434/pdf-translator
- PDF 레이아웃 분석: [DiT](https://github.com/microsoft/unilm) 사용
- PDF를 텍스트로 변환: [PaddlePaddle](https://github.com/PaddlePaddle/PaddleOCR) 모델 사용
