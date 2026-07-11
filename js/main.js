document.addEventListener('DOMContentLoaded', () => {
  // ==========================================================================
  // DOM Elements
  // ==========================================================================
  const navLinks = document.querySelectorAll('.nav-link');
  const coachingForm = document.getElementById('coaching-form');
  const jobInput = document.getElementById('job-input');
  const skillsInput = document.getElementById('skills-input');
  const skillChips = document.querySelectorAll('.skill-chip');
  const experienceInput = document.getElementById('experience-input');
  const submitBtn = document.getElementById('submit-btn');
  const btnText = document.getElementById('btn-text');
  
  const resultEmpty = document.getElementById('result-empty');
  const resultLoading = document.getElementById('result-loading');
  const resultContent = document.getElementById('result-content');
  const errorBanner = document.getElementById('error-banner');
  const errorMessage = document.getElementById('error-message');
  const copyBtn = document.getElementById('copy-btn');
  
  const faqItems = document.querySelectorAll('.faq-item');
  const toast = document.getElementById('toast');
  const toastMessage = document.getElementById('toast-message');

  let rawAIResultText = ''; // Stores unparsed markdown for copy functionality

  // ==========================================================================
  // Skills Presets (Badge Chips) Controller
  // ==========================================================================
  skillChips.forEach(chip => {
    chip.addEventListener('click', () => {
      const skillName = chip.getAttribute('data-skill');
      let currentSkills = skillsInput.value.split(',')
                                    .map(s => s.trim())
                                    .filter(s => s !== '');

      const index = currentSkills.indexOf(skillName);
      if (index > -1) {
        // Remove if already exists
        currentSkills.splice(index, 1);
        chip.classList.remove('selected');
        showToast(`${skillName} 기술이 제외되었습니다.`, 'info');
      } else {
        // Add if not present
        currentSkills.push(skillName);
        chip.classList.add('selected');
        showToast(`${skillName} 기술이 추가되었습니다.`, 'success');
      }

      // Rebind to input box
      skillsInput.value = currentSkills.join(', ');
    });
  });

  // Track manual changes in skills input to update chip UI states
  skillsInput.addEventListener('input', () => {
    const currentSkills = skillsInput.value.split(',')
                                  .map(s => s.trim().toLowerCase());
    
    skillChips.forEach(chip => {
      const skillName = chip.getAttribute('data-skill').toLowerCase();
      if (currentSkills.includes(skillName)) {
        chip.classList.add('selected');
      } else {
        chip.classList.remove('selected');
      }
    });
  });

  // ==========================================================================
  // Navigation active state highlight on scroll
  // ==========================================================================
  const sections = document.querySelectorAll('section');
  
  window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.clientHeight;
      if (pageYOffset >= (sectionTop - 150)) {
        current = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href').includes(current)) {
        link.classList.add('active');
      }
    });
  });

  // Smooth scroll configuration
  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = link.getAttribute('href');
      const targetSection = document.querySelector(targetId);
      
      window.scrollTo({
        top: targetSection.offsetTop - 70,
        behavior: 'smooth'
      });
      
      navLinks.forEach(l => l.classList.remove('active'));
      link.classList.add('active');
    });
  });

  // ==========================================================================
  // FAQ Accordion Controller
  // ==========================================================================
  faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');
    question.addEventListener('click', () => {
      const isOpen = item.classList.contains('open');
      
      // Close all other items first (accordion effect)
      faqItems.forEach(otherItem => {
        otherItem.classList.remove('open');
      });

      if (!isOpen) {
        item.classList.add('open');
      }
    });
  });

  // ==========================================================================
  // AI Form Submit & API Call
  // ==========================================================================
  coachingForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // 1. Client-side input validation
    const job = jobInput.value.trim();
    const skills = skillsInput.value.trim();
    const experience = experienceInput.value.trim();

    if (!job || !skills || !experience) {
      showErrorBanner('모든 필드를 정상적으로 채워주세요. 빈 입력은 분석할 수 없습니다.');
      return;
    }

    // 2. Set UI loading states
    setUIState('loading');
    
    // 3. Perform asynchronous API fetch with Timeout (25 seconds)
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 25000);

    try {
      const response = await fetch('/api/coach', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ job, skills, experience }),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || `서버 오류 발생 (${response.status})`);
      }

      if (data.success && data.result) {
        // 4. Render markdown result on success
        rawAIResultText = data.result;
        resultContent.innerHTML = marked.parse(data.result);
        setUIState('success');
        showToast('성공적으로 분석 가이드가 수립되었습니다!', 'success');
      } else {
        throw new Error('올바르지 않은 데이터 응답 구조입니다.');
      }

    } catch (error) {
      clearTimeout(timeoutId);
      setUIState('error');
      
      // Categorize and display error message
      if (error.name === 'AbortError') {
        showErrorBanner('응답 지연: AI 모델의 연동 지연(타임아웃)이 발생했습니다. 다시 시도해 주세요.');
      } else {
        showErrorBanner(`오류: ${error.message || '네트워크 통신 중 문제가 발생했습니다.'}`);
      }
    }
  });

  // Helper to switch result panel displays
  function setUIState(state) {
    // Enable/disable form components
    const inputs = [jobInput, skillsInput, experienceInput];
    
    if (state === 'loading') {
      submitBtn.disabled = true;
      inputs.forEach(input => input.disabled = true);
      btnText.innerText = 'AI 컨설턴트 분석 중...';
      
      resultEmpty.classList.add('d-none');
      resultContent.classList.add('d-none');
      errorBanner.classList.add('d-none');
      resultLoading.classList.remove('d-none');
      copyBtn.disabled = true;
    } else {
      submitBtn.disabled = false;
      inputs.forEach(input => input.disabled = false);
      btnText.innerText = '코칭 분석 받기';
      resultLoading.classList.add('d-none');
      
      if (state === 'success') {
        resultContent.classList.remove('d-none');
        copyBtn.disabled = false;
      } else if (state === 'error') {
        resultEmpty.classList.remove('d-none');
        copyBtn.disabled = true;
      }
    }
  }

  function showErrorBanner(message) {
    errorMessage.innerText = message;
    errorBanner.classList.remove('d-none');
    
    // Smooth scroll to view error banner on mobile
    if (window.innerWidth < 992) {
      errorBanner.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }

  // ==========================================================================
  // Copy to Clipboard Controller
  // ==========================================================================
  copyBtn.addEventListener('click', () => {
    if (!rawAIResultText) return;
    
    navigator.clipboard.writeText(rawAIResultText)
      .then(() => {
        showToast('클립보드에 마크다운이 복사되었습니다!', 'success');
      })
      .catch(err => {
        showToast('복사에 실패했습니다. 직접 드래그 복사를 이용해 주세요.', 'error');
      });
  });

  // ==========================================================================
  // Toast System
  // ==========================================================================
  let toastTimer;
  function showToast(message, type = 'success') {
    clearTimeout(toastTimer);
    
    const icon = toast.querySelector('.toast-icon');
    toastMessage.innerText = message;
    
    if (type === 'success') {
      icon.className = 'fa-solid fa-circle-check toast-icon';
      icon.style.color = 'var(--success-text)';
      toast.style.borderColor = 'var(--success-border)';
    } else if (type === 'error') {
      icon.className = 'fa-solid fa-circle-xmark toast-icon';
      icon.style.color = 'var(--error-text)';
      toast.style.borderColor = 'var(--error-border)';
    } else {
      icon.className = 'fa-solid fa-circle-info toast-icon';
      icon.style.color = 'var(--primary-color)';
      toast.style.borderColor = 'rgba(255, 84, 0, 0.2)';
    }

    toast.classList.add('show');
    
    toastTimer = setTimeout(() => {
      toast.classList.remove('show');
    }, 3000);
  }
});
