import numpy as np

def calculate_max_deflection(w, L, E, I):
    """
    등분포 하중을 받는 단순 지지보의 최대 처짐량 계산
    
    Parameters:
    w: 등분포 하중 (N/m)
    L: 보의 길이 (m)
    E: 탄성계수 (Pa)
    I: 단면 2차 모멘트 (m^4)
    
    Returns:
    최대 처짐량 (m)
    """
    # 최대 처짐량 공식: δ_max = (5wL^4) / (384EI)
    max_deflection = (5 * w * L**4) / (384 * E * I)
    return max_deflection

def calculate_deflection(x, w, L, E, I):
    """
    보의 길이에 따른 처짐량 계산
    
    Parameters:
    x: 보의 길이 위의 위치 (m) - numpy array 또는 scalar
    w: 등분포 하중 (N/m)
    L: 보의 길이 (m)
    E: 탄성계수 (Pa)
    I: 단면 2차 모멘트 (m^4)
    
    Returns:
    처짐량 (m) - numpy array 또는 scalar
    """
    # 처짐 함수: y(x) = (w/24EI)(x^4 - 2Lx^3 + L^3x)
    deflection = (w / (24 * E * I)) * (x**4 - 2*L*x**3 + L**3*x)
    return deflection

def calculate_shear_force(x, w, L):
    """
    전단력 계산 (참고용)
    
    Parameters:
    x: 보의 길이 위의 위치 (m)
    w: 등분포 하중 (N/m)
    L: 보의 길이 (m)
    
    Returns:
    전단력 (N)
    """
    # V(x) = wL/2 - wx
    shear_force = w * L / 2 - w * x
    return shear_force

def calculate_bending_moment(x, w, L):
    """
    휨모멘트 계산 (참고용)
    
    Parameters:
    x: 보의 길이 위의 위치 (m)
    w: 등분포 하중 (N/m)
    L: 보의 길이 (m)
    
    Returns:
    휨모멘트 (N·m)
    """
    # M(x) = (wL/2)x - (w/2)x^2
    bending_moment = (w * L / 2) * x - (w / 2) * x**2
    return bending_moment

def validate_inputs(L, E, I, w):
    """
    입력값 유효성 검사
    
    Parameters:
    L, E, I, w: 입력값들
    
    Returns:
    bool: 유효한 입력인지 여부
    """
    if L <= 0 or E <= 0 or I <= 0 or w <= 0:
        return False
    return True

def get_material_properties(material_name):
    """
    일반적인 재료의 탄성계수 반환 (참고용)
    
    Parameters:
    material_name: 재료명
    
    Returns:
    탄성계수 (Pa)
    """
    materials = {
        'steel': 2.1e11,      # 철
        'aluminum': 7.0e10,   # 알루미늄
        'concrete': 3.0e10,   # 콘크리트
        'wood': 1.2e10,       # 목재
        'glass': 7.0e10       # 유리
    }
    return materials.get(material_name.lower(), 2.1e11)

def get_practical_examples():
    """
    실제 사용할 만한 값들의 예시 반환
    
    Returns:
    dict: 실용적인 입력값 예시들
    """
    examples = {
        'steel_beam': {
            'name': '철제 보 (건축용)',
            'length': 6.0,           # 6m
            'elastic_modulus': 2.1e11,  # 철의 탄성계수
            'moment_of_inertia': 1.2e-5,  # I-beam 단면
            'load': 8000,            # 8 kN/m
            'description': '건축물의 철제 보 (I-beam)'
        },
        'concrete_beam': {
            'name': '콘크리트 보 (교량용)',
            'length': 12.0,          # 12m
            'elastic_modulus': 3.0e10,   # 콘크리트 탄성계수
            'moment_of_inertia': 5.0e-4,  # 직사각형 단면
            'load': 15000,           # 15 kN/m
            'description': '교량의 콘크리트 보'
        },
        'wooden_beam': {
            'name': '목재 보 (주택용)',
            'length': 4.0,           # 4m
            'elastic_modulus': 1.2e10,   # 목재 탄성계수
            'moment_of_inertia': 2.5e-6,  # 직사각형 단면
            'load': 2000,            # 2 kN/m
            'description': '주택의 목재 보'
        },
        'aluminum_beam': {
            'name': '알루미늄 보 (경량 구조)',
            'length': 3.0,           # 3m
            'elastic_modulus': 7.0e10,   # 알루미늄 탄성계수
            'moment_of_inertia': 8.5e-7,  # 박스 단면
            'load': 3000,            # 3 kN/m
            'description': '경량 구조물의 알루미늄 보'
        },
        'glass_beam': {
            'name': '유리 보 (장식용)',
            'length': 2.0,           # 2m
            'elastic_modulus': 7.0e10,   # 유리 탄성계수
            'moment_of_inertia': 1.0e-7,  # 직사각형 단면
            'load': 1000,            # 1 kN/m
            'description': '장식용 유리 보'
        }
    }
    return examples

def get_beam_section_properties(beam_type):
    """
    일반적인 보 단면의 2차 모멘트 값들
    
    Parameters:
    beam_type: 보 단면 타입
    
    Returns:
    단면 2차 모멘트 (m^4)
    """
    sections = {
        'rectangular': {
            'small': 1.0e-6,    # 10cm x 20cm
            'medium': 1.0e-5,   # 15cm x 30cm
            'large': 1.0e-4     # 20cm x 40cm
        },
        'i_beam': {
            'small': 5.0e-6,    # 작은 I-beam
            'medium': 1.2e-5,   # 중간 I-beam
            'large': 3.0e-5     # 큰 I-beam
        },
        'circular': {
            'small': 2.0e-6,    # 지름 10cm
            'medium': 1.0e-5,   # 지름 15cm
            'large': 5.0e-5     # 지름 20cm
        }
    }
    return sections.get(beam_type, sections['rectangular']) 