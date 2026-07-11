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
  const emailInput = document.getElementById('email-input');
  const submitBtn = document.getElementById('submit-btn');
  const btnText = document.getElementById('btn-text');
  
  const resultEmpty = document.getElementById('result-empty');
  const resultLoading = document.getElementById('result-loading');
  const resultContent = document.getElementById('result-content');
  const errorBanner = document.getElementById('error-banner');
  const errorMessage = document.getElementById('error-message');
  const copyBtn = document.getElementById('copy-btn');
  const randomBtn = document.getElementById('random-btn');
  const themeToggle = document.getElementById('theme-toggle');
  
  const faqItems = document.querySelectorAll('.faq-item');
  const toast = document.getElementById('toast');
  const toastMessage = document.getElementById('toast-message');
  
  const newsLoading = document.getElementById('news-loading');
  const newsList = document.getElementById('news-list');
  const currentTimeEl = document.getElementById('current-time');

  let rawAIResultText = ''; // Stores unparsed markdown for copy functionality

  // ==========================================================================
  // Dark/Light Hybrid Theme Controller
  // ==========================================================================
  if (themeToggle) {
    const themeIcon = themeToggle.querySelector('i');
    
    // Restore user theme from localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      document.body.classList.add('dark-mode');
      if (themeIcon) {
        themeIcon.className = 'fa-solid fa-sun';
      }
    }

    themeToggle.addEventListener('click', () => {
      const isDark = document.body.classList.toggle('dark-mode');
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
      
      if (themeIcon) {
        themeIcon.className = isDark ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
      }
      showToast(isDark ? '🌙 다크 모드가 활성화되었습니다.' : '☀️ 라이트 모드가 활성화되었습니다.', 'success');
    });
  }

  // ==========================================================================
  // Real-time Clock Controller for Trend Header
  // ==========================================================================
  function updateClock() {
    if (!currentTimeEl) return;
    const now = new Date();
    const yyyy = now.getFullYear();
    const mm = String(now.getMonth() + 1).padStart(2, '0');
    const dd = String(now.getDate()).padStart(2, '0');
    const hh = String(now.getHours()).padStart(2, '0');
    const min = String(now.getMinutes()).padStart(2, '0');
    const ss = String(now.getSeconds()).padStart(2, '0');
    currentTimeEl.innerText = `${yyyy}.${mm}.${dd} ${hh}:${min}:${ss}`;
  }
  updateClock();
  setInterval(updateClock, 1000);

  // ==========================================================================
  // Real-time Tech & Career News RSS Loader
  // ==========================================================================
  function formatPubDate(rawDate) {
    if (!rawDate) return '';
    try {
      const d = new Date(rawDate);
      if (isNaN(d.getTime())) return rawDate;
      const month = String(d.getMonth() + 1).padStart(2, '0');
      const day = String(d.getDate()).padStart(2, '0');
      return `${month}.${day}`;
    } catch {
      return rawDate;
    }
  }

  async function fetchTrendNews() {
    if (!newsLoading || !newsList) return;
    
    try {
      const response = await fetch('/api/news');
      if (!response.ok) throw new Error('API response failed');
      
      const data = await response.json();
      if (data.success && data.news && data.news.length > 0) {
        // 날짜 내림차순 (최신순) 정렬 보정
        data.news.sort((a, b) => new Date(b.pubDate) - new Date(a.pubDate));

        newsList.innerHTML = '';
        data.news.forEach((item, index) => {
          const li = document.createElement('li');
          li.className = 'news-item';
          li.style.animationDelay = `${index * 0.08}s`; // Stagger animation
          
          li.innerHTML = `
            <a href="${item.link}" target="_blank" class="news-link" title="${item.title}">
              ${item.title}
            </a>
            <div class="news-meta">
              <span class="news-source"><i class="fa-solid fa-hashtag"></i> ${item.source}</span>
              <span class="news-date">${formatPubDate(item.pubDate)}</span>
            </div>
          `;
          newsList.appendChild(li);
        });
        
        newsLoading.classList.add('d-none');
        newsList.classList.remove('d-none');
      } else {
        throw new Error('No news data');
      }
    } catch (err) {
      console.warn('Failed to load live RSS feed, utilizing fallback. error:', err);
      // Fallback UI static rendering directly from fallback list if network fails
      renderFallbackNews();
    }
  }

  function renderFallbackNews() {
    const fallbackData = [
      { title: "2026 하반기 채용 트렌드: AI 기술 면접 대비와 돋보이는 포트폴리오 기획법", link: "https://www.wanted.co.kr", pubDate: "Sun, 12 Jul 2026", source: "원티드" },
      { title: "성공적인 연봉 협상과 커리어 퀀텀 점프를 위한 이직 시나리오 가이드", link: "https://www.rememberapp.co.kr", pubDate: "Sat, 11 Jul 2026", source: "리멤버" },
      { title: "1인 테크 창업 및 사이드 프로젝트로 완성하는 나만의 포트폴리오 노하우", link: "https://www.wanted.co.kr", pubDate: "Fri, 10 Jul 2026", source: "스타트업레시피" }
    ];
    
    newsList.innerHTML = '';
    fallbackData.forEach((item, index) => {
      const li = document.createElement('li');
      li.className = 'news-item';
      li.style.animationDelay = `${index * 0.08}s`;
      li.innerHTML = `
        <a href="${item.link}" target="_blank" class="news-link" title="${item.title}">
          ${item.title}
        </a>
        <div class="news-meta">
          <span class="news-source"><i class="fa-solid fa-hashtag"></i> ${item.source}</span>
          <span class="news-date">${formatPubDate(item.pubDate)}</span>
        </div>
      `;
      newsList.appendChild(li);
    });
    newsLoading.classList.add('d-none');
    newsList.classList.remove('d-none');
  }

  // Initial trigger for live RSS Feed fetching
  fetchTrendNews();

  // ==========================================================================
  // Sample Data for Random Generator
  // ==========================================================================
  const sampleData = [
    {
      job: "프론트엔드 개발자",
      skills: "React, TypeScript, TailwindCSS",
      experience: "3개월간 쇼핑몰 프로젝트 진행. 결제 모듈 연동 시 CORS 네트워크 장애를 분석하여 프록시 서버 우회 설정으로 해결함. 페이지 로딩 속도를 1.5초 단축하여 사용자 전환율 개선에 기여."
    },
    {
      job: "백엔드 파이썬 개발자",
      skills: "Python, Django, PostgreSQL, Docker",
      experience: "6개월간 물류 관리 플랫폼 배송 조회 API 구축. 데이터베이스 쿼리를 리팩토링하고 주요 외래키 인덱싱 처리를 추가하여 쿼리 실행 속도를 기존 대비 40% 향상시켰으며 서버 부하를 안정화함."
    },
    {
      job: "데이터 엔지니어",
      skills: "Python, SQL, Apache Spark, Airflow",
      experience: "4개월 동안 대용량 실시간 에러 로그 수집 파이프라인 자동화 구현. 매일 50GB 가량의 정형/비정형 데이터를 클렌징하고 저장하는 스케줄링을 구축하여 기존 일 수작업 보고 단계를 자동 통계 리포트로 개선."
    },
    {
      job: "UI/UX 디자이너",
      skills: "Figma, CSS3, HTML5",
      experience: "2개월간 교육 매칭 서비스 메인 앱 화면 예약 흐름 개선. 사용자 인터뷰 리서치 기반으로 결제 단계를 기존 5단계에서 2단계로 간소화 설계하여 최종 회원가입 이후 결제 전환 성공률을 15% 이상 증대함."
    }
  ];

  let currentSampleIndex = -1;

  // Auto-fill random template with updateable input values
  function fillRandomExample(silent = false) {
    let randomIndex;
    do {
      randomIndex = Math.floor(Math.random() * sampleData.length);
    } while (randomIndex === currentSampleIndex && sampleData.length > 1);
    
    currentSampleIndex = randomIndex;
    const selected = sampleData[randomIndex];
    
    jobInput.value = selected.job;
    skillsInput.value = selected.skills;
    experienceInput.value = selected.experience;
    if (emailInput) emailInput.value = '';
    
    // Synchronize preset badge chip active states
    const activeSkills = selected.skills.split(',').map(s => s.trim().toLowerCase());
    skillChips.forEach(chip => {
      const skillName = chip.getAttribute('data-skill').toLowerCase();
      if (activeSkills.includes(skillName)) {
        chip.classList.add('selected');
      } else {
        chip.classList.remove('selected');
      }
    });

    if (!silent) {
      showToast('🎲 새로운 예시 데이터가 생성되었습니다!', 'success');
    }
  }

  // Load initial random example on DOM load silently
  fillRandomExample(true);

  // Bind click event to the dice button
  if (randomBtn) {
    randomBtn.addEventListener('click', () => {
      fillRandomExample(false);
    });
  }

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
    const email = emailInput ? emailInput.value.trim() : '';

    if (!job || !skills || !experience) {
      showErrorBanner('모든 필드를 정상적으로 채워주세요. 빈 입력은 분석할 수 없습니다.');
      return;
    }

    // 2. Set UI loading states
    setUIState('loading');
    
    // 3. Perform asynchronous API fetch with Timeout (60 seconds)
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 60000);

    try {
      const response = await fetch('/api/coach', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ job, skills, experience, email }),
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
