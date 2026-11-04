/* 现金 / 赎回在途（C1）。金额是估算：11/03 净值 × 份额，确认到账后改 status / confirmedAmount。 */
window.REDEMPTIONS = {
  "asOf": "2026-11-04",
  "note": "支付宝 13:52–14:00 已提交；金额按 11/03 净值×份额粗算，11/04 确认净值到账后请改 status/confirmedAmount",
  "cashTargetPct": 0.12,
  "redemptions": [
    {
      "date": "2026-11-04",
      "account": "支付宝",
      "code": "017811",
      "name": "东方人工智能主题混合C",
      "shares": 129294.89,
      "navRefDate": "2026-11-03",
      "navRef": 2.0023,
      "amountEst": 258887,
      "status": "已提交",
      "expectedArrive": "2026-11-05"
    },
    {
      "date": "2026-11-04",
      "account": "支付宝",
      "code": "006503",
      "name": "财通集成电路产业股票C",
      "shares": 62492.56,
      "navRefDate": "2026-11-03",
      "navRef": 3.6473,
      "amountEst": 227929,
      "status": "已提交",
      "expectedArrive": "2026-11-05"
    },
    {
      "date": "2026-11-04",
      "account": "支付宝",
      "code": "005661",
      "name": "嘉实资源精选股票C",
      "shares": 63325.31,
      "navRefDate": "2026-11-03",
      "navRef": 4.0121,
      "amountEst": 254067,
      "status": "已提交",
      "expectedArrive": "2026-11-05"
    },
    {
      "date": "2026-11-04",
      "account": "支付宝",
      "code": "008619",
      "name": "永赢医药健康C",
      "shares": 37189.24,
      "navRefDate": "2026-11-03",
      "navRef": 1.0976,
      "amountEst": 40819,
      "status": "已提交",
      "expectedArrive": "2026-11-05"
    },
    {
      "date": "2026-11-04",
      "account": "支付宝",
      "code": "019671",
      "name": "广发港股创新药ETF联接(QDII)C",
      "shares": 16781.34,
      "navRefDate": "2026-11-03",
      "navRef": 1.1869,
      "amountEst": 19918,
      "status": "已提交",
      "expectedArrive": "2026-11-06"
    },
    {
      "date": "2026-11-04",
      "account": "支付宝",
      "code": "003231",
      "name": "创金合信医疗保健行业股票C",
      "shares": 10236.84,
      "navRefDate": "2026-11-03",
      "navRef": 1.5091,
      "amountEst": 15448,
      "status": "已提交",
      "expectedArrive": "2026-11-05"
    }
  ],
  "amountEstTotal": 817068,
  "ops": {
    "doNotRebuyIcAiToday": true,
    "qdiiDefaultHold": true,
    "remainingFocus": ["018036", "006373", "539002", "017731", "018147"]
  }
};
