from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 백엔드에서 사용하기 위해
import matplotlib.font_manager as fm
import io
import base64
from utils.beam import calculate_deflection, calculate_max_deflection

# 한글 폰트 설정
def setup_korean_font():
    """한글 폰트 설정"""
    # Windows에서 사용 가능한 한글 폰트들
    korean_fonts = ['Malgun Gothic', 'NanumGothic', 'NanumBarunGothic', 'Batang', 'Dotum']
    
    for font in korean_fonts:
        try:
            plt.rcParams['font.family'] = font
            plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
            break
        except:
            continue
    
    # 폰트가 설정되지 않았으면 기본 폰트 사용
    if plt.rcParams['font.family'] == 'DejaVu Sans':
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'DejaVu Sans']

# 한글 폰트 설정 적용
setup_korean_font()

app = Flask(__name__)

@app.route('/')
def index():
    """메인 페이지 - 입력 폼 제공"""
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """보의 처짐 계산 및 시각화"""
    try:
        # 폼 데이터 받기
        L = float(request.form['length'])  # 보의 길이 (m)
        E = float(request.form['elastic_modulus'])  # 탄성계수 (Pa)
        I = float(request.form['moment_of_inertia'])  # 단면 2차 모멘트 (m^4)
        w = float(request.form['load'])  # 등분포 하중 (N/m)
        
        # 입력값 검증
        if L <= 0 or E <= 0 or I <= 0 or w <= 0:
            return render_template('index.html', 
                                error="모든 값은 양수여야 합니다.")
        
        # 최대 처짐량 계산
        max_deflection = calculate_max_deflection(w, L, E, I)
        
        # 처짐 곡선 데이터 생성
        x_points = np.linspace(0, L, 100)
        y_points = calculate_deflection(x_points, w, L, E, I)
        
        # 그래프 생성
        plt.figure(figsize=(10, 6))
        plt.plot(x_points, y_points, 'b-', linewidth=2, label='처짐 곡선')
        plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
        plt.axvline(x=L, color='k', linestyle='-', alpha=0.3)
        
        plt.xlabel('보의 길이 (m)')
        plt.ylabel('처짐량 (m)')
        plt.title('등분포 하중을 받는 단순 지지보의 처짐 곡선')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # 그래프를 이미지로 변환
        img = io.BytesIO()
        plt.savefig(img, format='png', dpi=300, bbox_inches='tight')
        img.seek(0)
        plt.close()
        
        # Base64로 인코딩
        graph_url = base64.b64encode(img.getvalue()).decode()
        
        return render_template('index.html',
                             length=L,
                             elastic_modulus=E,
                             moment_of_inertia=I,
                             load=w,
                             max_deflection=max_deflection,
                             graph_url=graph_url)
    
    except ValueError:
        return render_template('index.html', 
                            error="올바른 숫자를 입력해주세요.")
    except Exception as e:
        return render_template('index.html', 
                            error=f"계산 중 오류가 발생했습니다: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True) 