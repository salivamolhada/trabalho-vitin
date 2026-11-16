import React, { useEffect, useMemo, useState } from 'react';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import {
  AlertTriangle,
  BarChart3,
  Calendar,
  CheckCircle2,
  Edit3,
  Gift,
  HeartHandshake,
  Info,
  LayoutDashboard,
  Menu,
  Package,
  Plus,
  RotateCcw,
  Search,
  Sparkles,
  Trash2,
  X,
} from 'lucide-react';
import {
  CATEGORIAS_META,
  CategoriaTipo,
  DistribuicaoRecord,
  DoacaoRecord,
  EstoqueMap,
  FRASES_SOLIDARIEDADE,
  createInitialSeed,
} from './data/initialData';

type ScreenKey = 'dashboard' | 'doacoes' | 'estoque' | 'distribuicoes' | 'graficos' | 'sobre';

interface PopupState {
  open: boolean;
  titulo: string;
  mensagem: string;
  icone: string;
  tipo: 'sucesso' | 'erro';
}

const STORAGE_KEY = 'solidario_tech_python_sim_v1';

const SNOWFLAKES = [
  { left: '4%', size: '13px', duration: '15s', delay: '0s', drift: '20px', opacity: 0.45 },
  { left: '14%', size: '16px', duration: '19s', delay: '-4s', drift: '-24px', opacity: 0.35 },
  { left: '25%', size: '11px', duration: '14s', delay: '-8s', drift: '18px', opacity: 0.5 },
  { left: '38%', size: '15px', duration: '21s', delay: '-2s', drift: '-18px', opacity: 0.3 },
  { left: '52%', size: '12px', duration: '16s', delay: '-6s', drift: '26px', opacity: 0.45 },
  { left: '66%', size: '17px', duration: '22s', delay: '-11s', drift: '-22px', opacity: 0.35 },
  { left: '78%', size: '12px', duration: '15s', delay: '-3s', drift: '16px', opacity: 0.5 },
  { left: '91%', size: '14px', duration: '18s', delay: '-9s', drift: '-20px', opacity: 0.4 },
];

const BULB_COLORS = ['#F59E0B', '#E11D48', '#10B981', '#FBBF24', '#38BDF8', '#D4AF37'];

function formatarDataBR(iso: string): string {
  const parts = iso.slice(0, 10).split('-');
  if (parts.length !== 3) return iso;
  return `${parts[2]}/${parts[1]}/${parts[0]}`;
}

function diasParaNatal(): number {
  const hoje = new Date();
  const base = new Date(hoje.getFullYear(), hoje.getMonth(), hoje.getDate());
  let natal = new Date(hoje.getFullYear(), 11, 25);
  if (base > natal) {
    natal = new Date(hoje.getFullYear() + 1, 11, 25);
  }
  return Math.round((natal.getTime() - base.getTime()) / (1000 * 60 * 60 * 24));
}

function PineGiftLogo() {
  return (
    <svg width="42" height="42" viewBox="0 0 64 64" fill="none" aria-hidden="true">
      <circle cx="32" cy="32" r="30" fill="#F8FAFC" stroke="#D4AF37" strokeWidth="2.5" />
      <polygon points="32,8 34.5,13.5 40,13.5 35.5,17 37,22.5 32,19 27,22.5 28.5,17 24,13.5 29.5,13.5" fill="#D4AF37" />
      <polygon points="32,16 18,32 46,32" fill="#177557" />
      <polygon points="32,24 14,42 50,42" fill="#0B3D2E" />
      <rect x="29" y="42" width="6" height="6" fill="#704424" />
      <rect x="23" y="45" width="18" height="12" rx="2" fill="#C1272D" stroke="#FFFFFF" strokeWidth="1.2" />
      <rect x="30.5" y="45" width="3" height="12" fill="#D4AF37" />
      <rect x="23" y="49.5" width="18" height="3" fill="#D4AF37" />
    </svg>
  );
}

/** Cordão de pisca-pisca natalino reutilizável para cabeçalhos e cards de itens */
function PiscaPiscaStrip({
  count = 9,
  compact = false,
}: {
  count?: number;
  compact?: boolean;
}) {
  return (
    <div
      className={`relative flex items-center justify-between w-full overflow-hidden select-none pointer-events-none ${
        compact ? 'px-3 pt-1.5 pb-1' : 'px-5 py-1.5'
      }`}
      aria-hidden="true"
    >
      {/* Fio prateado/dourado conectando as lâmpadas */}
      <div
        className={`absolute left-2 right-2 border-t border-slate-300/80 ${
          compact ? 'top-2.5' : 'top-3'
        }`}
      />
      {Array.from({ length: count }).map((_, idx) => {
        const color = BULB_COLORS[idx % BULB_COLORS.length];
        const delay = `${((idx % 4) * 0.35).toFixed(2)}s`;
        const duration = `${(1.25 + (idx % 3) * 0.3).toFixed(2)}s`;
        return (
          <span key={idx} className="relative z-10 flex flex-col items-center">
            <span className="w-1.5 h-1 bg-slate-400 rounded-t-xs" />
            <span
              className={`pisca-bulb rounded-full ${compact ? 'w-2 h-2.5' : 'w-2.5 h-3'}`}
              style={
                {
                  backgroundColor: color,
                  color,
                  '--twinkle-delay': delay,
                  '--twinkle-duration': duration,
                } as React.CSSProperties
              }
            />
          </span>
        );
      })}
    </div>
  );
}

export default function App() {
  const [screen, setScreen] = useState<ScreenKey>('dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [luzesAtivas, setLuzesAtivas] = useState(true);

  const [doacoes, setDoacoes] = useState<DoacaoRecord[]>(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) return JSON.parse(raw).doacoes;
    } catch {
      /* ignore */
    }
    return createInitialSeed().doacoes;
  });

  const [distribuicoes, setDistribuicoes] = useState<DistribuicaoRecord[]>(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) return JSON.parse(raw).distribuicoes;
    } catch {
      /* ignore */
    }
    return createInitialSeed().distribuicoes;
  });

  const [estoque, setEstoque] = useState<EstoqueMap>(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) return JSON.parse(raw).estoque;
    } catch {
      /* ignore */
    }
    return createInitialSeed().estoque;
  });

  const [fraseIdx, setFraseIdx] = useState(0);
  const [popup, setPopup] = useState<PopupState>({
    open: false,
    titulo: '',
    mensagem: '',
    icone: '🎁',
    tipo: 'sucesso',
  });

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({ doacoes, distribuicoes, estoque }));
    } catch {
      /* ignore */
    }
  }, [doacoes, distribuicoes, estoque]);

  useEffect(() => {
    const timer = setInterval(() => {
      setFraseIdx((prev) => (prev + 1) % FRASES_SOLIDARIEDADE.length);
    }, 8000);
    return () => clearInterval(timer);
  }, []);

  // Doacoes form & filters
  const [editId, setEditId] = useState<number | null>(null);
  const [doador, setDoador] = useState('');
  const [tipo, setTipo] = useState<CategoriaTipo>('brinquedo');
  const [quantidade, setQuantidade] = useState('');
  const [dataDoacao, setDataDoacao] = useState(() => new Date().toISOString().slice(0, 10));
  const [descricao, setDescricao] = useState('');
  const [buscaDoador, setBuscaDoador] = useState('');
  const [filtroTipo, setFiltroTipo] = useState<'todos' | CategoriaTipo>('todos');

  // Estoque manual adjustment
  const [ajusteTipo, setAjusteTipo] = useState<CategoriaTipo>('brinquedo');
  const [ajusteQtd, setAjusteQtd] = useState('');

  // Distribuicoes form & filter
  const [distTipo, setDistTipo] = useState<CategoriaTipo>('brinquedo');
  const [distQtd, setDistQtd] = useState('');
  const [beneficiario, setBeneficiario] = useState('');
  const [dataEntrega, setDataEntrega] = useState(() => new Date().toISOString().slice(0, 10));
  const [responsavel, setResponsavel] = useState('');
  const [buscaBeneficiario, setBuscaBeneficiario] = useState('');

  const showPopup = (
    titulo: string,
    mensagem: string,
    icone = '🎁',
    tipoPopup: 'sucesso' | 'erro' = 'sucesso'
  ) => {
    setPopup({ open: true, titulo, mensagem, icone, tipo: tipoPopup });
  };

  const totalDoado = useMemo(
    () => doacoes.reduce((acc, d) => acc + d.quantidade, 0),
    [doacoes]
  );
  const totalDistribuido = useMemo(
    () => distribuicoes.reduce((acc, d) => acc + d.quantidade, 0),
    [distribuicoes]
  );
  const totalEstoque = useMemo(
    () => (Object.values(estoque) as number[]).reduce((acc, n) => acc + n, 0),
    [estoque]
  );
  const categoriasBaixas = useMemo(
    () => (Object.keys(estoque) as CategoriaTipo[]).filter((k) => estoque[k] < 5),
    [estoque]
  );

  const doacoesFiltradas = useMemo(() => {
    return [...doacoes]
      .sort((a, b) => b.data_doacao.localeCompare(a.data_doacao) || b.id - a.id)
      .filter((d) => {
        const matchNome = d.doador.toLowerCase().includes(buscaDoador.trim().toLowerCase());
        const matchTipo = filtroTipo === 'todos' || d.tipo === filtroTipo;
        return matchNome && matchTipo;
      });
  }, [doacoes, buscaDoador, filtroTipo]);

  const ultimas5Doacoes = useMemo(() => {
    return [...doacoes]
      .sort((a, b) => b.data_doacao.localeCompare(a.data_doacao) || b.id - a.id)
      .slice(0, 5);
  }, [doacoes]);

  const distribuicoesFiltradas = useMemo(() => {
    return [...distribuicoes]
      .sort((a, b) => b.data_entrega.localeCompare(a.data_entrega) || b.id - a.id)
      .filter((d) =>
        d.beneficiario.toLowerCase().includes(buscaBeneficiario.trim().toLowerCase())
      );
  }, [distribuicoes, buscaBeneficiario]);

  const dadosPorCategoria = useMemo(() => {
    const somas: Record<CategoriaTipo, number> = {
      brinquedo: 0,
      alimento: 0,
      roupa: 0,
      dinheiro: 0,
      cesta: 0,
    };
    doacoes.forEach((d) => {
      somas[d.tipo] += d.quantidade;
    });
    return (Object.keys(CATEGORIAS_META) as CategoriaTipo[]).map((k) => ({
      categoria: CATEGORIAS_META[k].rotulo,
      quantidade: somas[k],
      cor: CATEGORIAS_META[k].cor,
    }));
  }, [doacoes]);

  const dadosUltimos30Dias = useMemo(() => {
    const mapa = new Map<string, number>();
    const hoje = new Date();
    for (let i = 29; i >= 0; i--) {
      const d = new Date(hoje);
      d.setDate(hoje.getDate() - i);
      mapa.set(d.toISOString().slice(0, 10), 0);
    }
    doacoes.forEach((d) => {
      if (mapa.has(d.data_doacao)) {
        mapa.set(d.data_doacao, (mapa.get(d.data_doacao) ?? 0) + d.quantidade);
      }
    });
    return Array.from(mapa.entries()).map(([iso, qtd]) => ({
      dia: `${iso.slice(8, 10)}/${iso.slice(5, 7)}`,
      quantidade: qtd,
    }));
  }, [doacoes]);

  const limparFormularioDoacao = () => {
    setEditId(null);
    setDoador('');
    setTipo('brinquedo');
    setQuantidade('');
    setDataDoacao(new Date().toISOString().slice(0, 10));
    setDescricao('');
  };

  const handleSalvarDoacao = (e: React.FormEvent) => {
    e.preventDefault();
    const qtd = Number(quantidade);
    if (doador.trim().length < 2) {
      showPopup('Campo Obrigatório', 'Informe o nome do doador (mínimo 2 caracteres).', '⚠️', 'erro');
      return;
    }
    if (!Number.isInteger(qtd) || qtd <= 0) {
      showPopup('Quantidade Inválida', 'A quantidade doada deve ser um número inteiro maior que zero.', '⚠️', 'erro');
      return;
    }
    if (!dataDoacao) {
      showPopup('Data Obrigatória', 'Informe a data da doação.', '⚠️', 'erro');
      return;
    }

    if (editId !== null) {
      const anterior = doacoes.find((d) => d.id === editId);
      if (!anterior) return;

      const novoEstoque = { ...estoque };
      if (anterior.tipo === tipo) {
        const delta = qtd - anterior.quantidade;
        if (novoEstoque[tipo] + delta < 0) {
          showPopup(
            'Estoque Insuficiente',
            `Não é possível reduzir esta doação porque parte dos itens de ${CATEGORIAS_META[tipo].rotulo} já foi distribuída.`,
            '⚠️',
            'erro'
          );
          return;
        }
        novoEstoque[tipo] += delta;
      } else {
        if (novoEstoque[anterior.tipo] - anterior.quantidade < 0) {
          showPopup(
            'Alteração Bloqueada',
            `Não há saldo suficiente em ${CATEGORIAS_META[anterior.tipo].rotulo} para estornar a categoria anterior.`,
            '⚠️',
            'erro'
          );
          return;
        }
        novoEstoque[anterior.tipo] -= anterior.quantidade;
        novoEstoque[tipo] += qtd;
      }

      setDoacoes((prev) =>
        prev.map((d) =>
          d.id === editId
            ? { ...d, doador: doador.trim(), tipo, quantidade: qtd, data_doacao: dataDoacao, descricao: descricao.trim() }
            : d
        )
      );
      setEstoque(novoEstoque);
      limparFormularioDoacao();
      showPopup('Doação Atualizada!', 'Registro atualizado e estoque recalculado automaticamente.', '🎁', 'sucesso');
    } else {
      const novoId = doacoes.reduce((max, d) => Math.max(max, d.id), 0) + 1;
      const nova: DoacaoRecord = {
        id: novoId,
        doador: doador.trim(),
        tipo,
        quantidade: qtd,
        data_doacao: dataDoacao,
        descricao: descricao.trim(),
      };
      setDoacoes((prev) => [nova, ...prev]);
      setEstoque((prev) => ({ ...prev, [tipo]: prev[tipo] + qtd }));
      limparFormularioDoacao();
      showPopup(
        'Doação Registrada!',
        `Doação de ${nova.doador} (${nova.quantidade}x ${CATEGORIAS_META[nova.tipo].rotulo}) salva e somada ao estoque.`,
        '🎁',
        'sucesso'
      );
    }
  };

  const handleExcluirDoacao = (item: DoacaoRecord) => {
    if (estoque[item.tipo] - item.quantidade < 0) {
      showPopup(
        'Exclusão Bloqueada',
        `Não é possível excluir porque ${item.quantidade} unidades de ${CATEGORIAS_META[item.tipo].rotulo} já foram distribuídas.`,
        '⚠️',
        'erro'
      );
      return;
    }
    setDoacoes((prev) => prev.filter((d) => d.id !== item.id));
    setEstoque((prev) => ({ ...prev, [item.tipo]: prev[item.tipo] - item.quantidade }));
    if (editId === item.id) limparFormularioDoacao();
    showPopup('Doação Excluída', 'Registro removido e saldo estornado do estoque.', '🎁', 'sucesso');
  };

  const handleAjusteEstoque = (sinal: 1 | -1) => {
    const qtd = Number(ajusteQtd);
    if (!Number.isInteger(qtd) || qtd <= 0) {
      showPopup('Valor Inválido', 'Informe uma quantidade inteira positiva para o ajuste manual.', '⚠️', 'erro');
      return;
    }
    const novoSaldo = estoque[ajusteTipo] + qtd * sinal;
    if (novoSaldo < 0) {
      showPopup(
        'Saldo Negativo Bloqueado',
        `Estoque disponível de ${CATEGORIAS_META[ajusteTipo].rotulo}: ${estoque[ajusteTipo]} un.`,
        '⚠️',
        'erro'
      );
      return;
    }
    setEstoque((prev) => ({ ...prev, [ajusteTipo]: novoSaldo }));
    setAjusteQtd('');
    showPopup(
      'Estoque Ajustado',
      `Novo saldo de ${CATEGORIAS_META[ajusteTipo].rotulo}: ${novoSaldo} un.`,
      '🎄',
      'sucesso'
    );
  };

  const handleRegistrarDistribuicao = (e: React.FormEvent) => {
    e.preventDefault();
    const qtd = Number(distQtd);
    if (!Number.isInteger(qtd) || qtd <= 0) {
      showPopup('Quantidade Inválida', 'Informe uma quantidade inteira maior que zero.', '⚠️', 'erro');
      return;
    }
    if (qtd > estoque[distTipo]) {
      showPopup(
        'Distribuição Bloqueada',
        `Estoque insuficiente para ${CATEGORIAS_META[distTipo].rotulo}! Disponível: ${estoque[distTipo]} | Solicitado: ${qtd}.`,
        '⚠️',
        'erro'
      );
      return;
    }
    if (beneficiario.trim().length < 2 || responsavel.trim().length < 2) {
      showPopup('Campos Obrigatórios', 'Informe o beneficiário e o responsável pela entrega.', '⚠️', 'erro');
      return;
    }

    const novoId = distribuicoes.reduce((max, d) => Math.max(max, d.id), 0) + 1;
    const nova: DistribuicaoRecord = {
      id: novoId,
      item_tipo: distTipo,
      quantidade: qtd,
      beneficiario: beneficiario.trim(),
      data_entrega: dataEntrega,
      responsavel: responsavel.trim(),
    };
    setDistribuicoes((prev) => [nova, ...prev]);
    setEstoque((prev) => ({ ...prev, [distTipo]: prev[distTipo] - qtd }));
    setDistQtd('');
    setBeneficiario('');
    setResponsavel('');
    showPopup(
      'Entrega Registrada!',
      `${nova.quantidade}x ${CATEGORIAS_META[nova.item_tipo].rotulo} entregues para ${nova.beneficiario}. Estoque atualizado!`,
      '⭐',
      'sucesso'
    );
  };

  const handleResetarDemo = () => {
    const seed = createInitialSeed();
    setDoacoes(seed.doacoes);
    setDistribuicoes(seed.distribuicoes);
    setEstoque(seed.estoque);
    limparFormularioDoacao();
    showPopup('Dados Restaurados', 'Banco de demonstração restaurado para o seed inicial.', '🎄', 'sucesso');
  };

  const navItems: { key: ScreenKey; label: string; icon: React.ReactNode }[] = [
    { key: 'dashboard', label: 'Dashboard', icon: <LayoutDashboard className="w-4 h-4" /> },
    { key: 'doacoes', label: 'Doações', icon: <Gift className="w-4 h-4" /> },
    { key: 'estoque', label: 'Estoque', icon: <Package className="w-4 h-4" /> },
    { key: 'distribuicoes', label: 'Distribuições', icon: <HeartHandshake className="w-4 h-4" /> },
    { key: 'graficos', label: 'Gráficos', icon: <BarChart3 className="w-4 h-4" /> },
    { key: 'sobre', label: 'Sobre & Python', icon: <Info className="w-4 h-4" /> },
  ];

  const titulos: Record<ScreenKey, string> = {
    dashboard: 'Painel Inicial — Natal Branco',
    doacoes: 'Cadastro e Gestão de Doações',
    estoque: 'Controle de Itens Disponíveis',
    distribuicoes: 'Registro de Distribuição Solidária',
    graficos: 'Relatórios e Gráficos Analíticos',
    sobre: 'Projeto Desktop Python & Arquitetura',
  };

  const hojeFormatado = new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  }).format(new Date());

  const contagemNatal = diasParaNatal();
  const taxaEntrega = totalDoado > 0 ? ((totalDistribuido / totalDoado) * 100).toFixed(1) : '0.0';

  return (
    <div className={`min-h-screen text-[#122620] flex relative ${luzesAtivas ? '' : 'pisca-paused'}`}>
      {/* Flocos de neve sutis do Natal Branco */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden z-0" aria-hidden="true">
        {SNOWFLAKES.map((flake, i) => (
          <span
            key={i}
            className="snowflake-particle"
            style={
              {
                left: flake.left,
                fontSize: flake.size,
                '--flake-duration': flake.duration,
                '--flake-delay': flake.delay,
                '--flake-drift': flake.drift,
                '--flake-opacity': flake.opacity,
              } as React.CSSProperties
            }
          >
            ❄
          </span>
        ))}
      </div>

      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-slate-900/30 backdrop-blur-[1px] z-30 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Left Sidebar — Natal Branco (Branco Neve + Prata + Ouro Champanhe) */}
      <aside
        className={`fixed lg:static inset-y-0 left-0 z-40 w-64 bg-white/95 backdrop-blur-md border-r border-slate-200/90 flex flex-col justify-between transition-transform duration-200 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        <div>
          <div className="px-5 py-5 flex items-center gap-3 border-b border-slate-200/80">
            <PineGiftLogo />
            <div>
              <div className="font-christmas text-2xl font-bold leading-none text-[#0B3D2E]">
                Solidário Tech
              </div>
              <div className="text-xs text-[#9A7B16] font-medium mt-1">Natal Branco 2026</div>
            </div>
          </div>

          <PiscaPiscaStrip count={7} compact />

          <nav className="p-3 space-y-1" aria-label="Navegação principal">
            {navItems.map((item) => {
              const ativo = screen === item.key;
              return (
                <button
                  key={item.key}
                  onClick={() => {
                    setScreen(item.key);
                    setSidebarOpen(false);
                  }}
                  className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors whitespace-nowrap shrink-0 cursor-pointer ${
                    ativo
                      ? 'bg-[#0B3D2E] text-white shadow-sm'
                      : 'text-[#334E45] hover:bg-slate-100 hover:text-[#0B3D2E]'
                  }`}
                >
                  {item.icon}
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>
        </div>

        <div className="p-4 m-3 rounded-xl bg-slate-50 border border-[#D4AF37]/50 text-xs text-[#4B635B] space-y-2">
          <div className="font-semibold text-[#0B3D2E]">Desafio Tech Solutions 2026</div>
          <div>3º A · Técnico em Desenvolvimento de Sistemas</div>
          <button
            onClick={handleResetarDemo}
            className="w-full mt-1 flex items-center justify-center gap-1.5 py-1.5 px-2.5 rounded-md bg-white border border-slate-200 hover:bg-slate-100 text-[#0B3D2E] font-medium transition-colors cursor-pointer whitespace-nowrap"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Restaurar Seed</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0 relative z-10">
        {/* Top Bar com Pisca-Pisca */}
        <header className="bg-white/90 backdrop-blur-md border-b border-slate-200/80 shrink-0">
          <PiscaPiscaStrip count={18} />
          <div className="h-14 px-4 lg:px-8 flex items-center justify-between gap-4">
            <div className="flex items-center gap-3 min-w-0">
              <button
                onClick={() => setSidebarOpen(true)}
                className="lg:hidden p-2 rounded-lg border border-slate-200 text-[#0B3D2E] cursor-pointer"
                aria-label="Abrir menu"
              >
                <Menu className="w-5 h-5" />
              </button>
              <h1 className="font-christmas text-2xl lg:text-3xl font-bold text-[#0B3D2E] truncate">
                {titulos[screen]}
              </h1>
            </div>

            <div className="flex items-center gap-3 shrink-0">
              <button
                onClick={() => setLuzesAtivas((v) => !v)}
                className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors cursor-pointer whitespace-nowrap ${
                  luzesAtivas
                    ? 'bg-amber-50 border-[#D4AF37] text-[#8C6D11]'
                    : 'bg-slate-100 border-slate-200 text-slate-600'
                }`}
              >
                <Sparkles className="w-3.5 h-3.5" />
                <span>{luzesAtivas ? 'Pisca-pisca ativo' : 'Luzes pausadas'}</span>
              </button>

              <span className="hidden sm:inline-flex items-center gap-1.5 text-xs lg:text-sm text-[#4B635B] font-mono tabular-nums whitespace-nowrap">
                <Calendar className="w-4 h-4 text-[#D4AF37]" />
                {hojeFormatado}
              </span>
            </div>
          </div>
        </header>

        <main className="flex-1 p-4 lg:p-7 max-w-[1320px] w-full mx-auto space-y-6 animate-fade-in">
          {/* SCREEN 1: DASHBOARD */}
          {screen === 'dashboard' && (
            <div className="space-y-6">
              {/* Banner Branco Neve com Pisca-Pisca */}
              <section className="bg-white rounded-2xl border border-[#D4AF37]/70 shadow-snow overflow-hidden">
                <PiscaPiscaStrip count={14} compact />
                <div className="px-6 py-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div className="space-y-1.5">
                    <h2 className="font-christmas text-3xl font-bold text-[#0B3D2E]">
                      🎄 Feliz Natal! Que a solidariedade transforme vidas.
                    </h2>
                    <p className="text-sm text-[#4B635B] italic">
                      ⭐ &ldquo;{FRASES_SOLIDARIEDADE[fraseIdx]}&rdquo;
                    </p>
                  </div>
                  <div className="bg-slate-50 border border-[#D4AF37] rounded-xl px-5 py-3 text-center shrink-0">
                    <div className="text-xs uppercase tracking-wider text-[#9A7B16] font-semibold">
                      Contagem Regressiva
                    </div>
                    <div className="font-mono tabular-nums text-lg font-bold text-[#C1272D]">
                      {contagemNatal === 0
                        ? '🎅 Hoje é Natal!'
                        : `🦌 ${contagemNatal} dias para 25/12`}
                    </div>
                  </div>
                </div>
              </section>

              {/* Cards de Resumo com Pisca-Pisca nos itens */}
              <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-white rounded-xl border border-slate-200 shadow-snow overflow-hidden">
                  <PiscaPiscaStrip count={7} compact />
                  <div className="p-5 pt-2">
                    <div className="text-xs font-medium text-[#4B635B]">
                      Total de Doações Recebidas
                    </div>
                    <div className="font-mono tabular-nums text-3xl font-bold text-[#0B3D2E] mt-1">
                      {totalDoado} <span className="text-base font-normal text-[#4B635B]">un.</span>
                    </div>
                    <div className="text-xs text-[#4B635B] mt-2">
                      {doacoes.length} registros cadastrados
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-xl border border-slate-200 shadow-snow overflow-hidden">
                  <PiscaPiscaStrip count={7} compact />
                  <div className="p-5 pt-2">
                    <div className="text-xs font-medium text-[#4B635B]">Total Distribuído</div>
                    <div className="font-mono tabular-nums text-3xl font-bold text-[#C1272D] mt-1">
                      {totalDistribuido}{' '}
                      <span className="text-base font-normal text-[#4B635B]">un.</span>
                    </div>
                    <div className="text-xs text-[#4B635B] mt-2">
                      {distribuicoes.length} entregas realizadas · {taxaEntrega}% do total
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-xl border border-slate-200 shadow-snow overflow-hidden">
                  <PiscaPiscaStrip count={7} compact />
                  <div className="p-5 pt-2">
                    <div className="text-xs font-medium text-[#4B635B]">Itens em Estoque</div>
                    <div className="font-mono tabular-nums text-3xl font-bold text-[#9A7B16] mt-1">
                      {totalEstoque}{' '}
                      <span className="text-base font-normal text-[#4B635B]">un.</span>
                    </div>
                    <div
                      className={`text-xs mt-2 font-medium ${
                        categoriasBaixas.length > 0 ? 'text-[#C1272D]' : 'text-[#0B3D2E]'
                      }`}
                    >
                      {categoriasBaixas.length > 0
                        ? `⚠️ ${categoriasBaixas.length} categoria(s) abaixo de 5 un.`
                        : 'Todas as categorias em nível adequado'}
                    </div>
                  </div>
                </div>
              </section>

              {/* Mini-cards das 5 categorias no Dashboard com pisca-pisca nos itens */}
              <section className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
                {(Object.keys(CATEGORIAS_META) as CategoriaTipo[]).map((cat) => {
                  const qtd = estoque[cat];
                  const baixo = qtd < 5;
                  return (
                    <button
                      key={cat}
                      onClick={() => setScreen('estoque')}
                      className={`text-left rounded-xl border shadow-snow overflow-hidden transition-transform hover:-translate-y-0.5 cursor-pointer ${
                        baixo
                          ? 'bg-[#FFF5F5] border-[#C1272D]/70'
                          : 'bg-white border-slate-200 hover:border-[#D4AF37]'
                      }`}
                    >
                      <PiscaPiscaStrip count={5} compact />
                      <div className="px-4 pb-3.5 pt-1">
                        <div className="text-xs font-semibold text-[#0B3D2E] flex items-center gap-1.5">
                          <span>{CATEGORIAS_META[cat].emoji}</span>
                          <span>{CATEGORIAS_META[cat].rotulo}</span>
                        </div>
                        <div
                          className={`font-mono tabular-nums text-xl font-bold mt-1 ${
                            baixo ? 'text-[#C1272D]' : 'text-[#122620]'
                          }`}
                        >
                          {qtd} un.
                        </div>
                      </div>
                    </button>
                  );
                })}
              </section>

              <section className="bg-white rounded-xl border border-slate-200 shadow-snow overflow-hidden">
                <div className="px-5 py-4 border-b border-slate-200 flex items-center justify-between">
                  <h3 className="font-semibold text-[#0B3D2E]">
                    🎁 Últimos 5 Registros de Doação
                  </h3>
                  <button
                    onClick={() => setScreen('doacoes')}
                    className="text-xs font-semibold text-[#0B3D2E] hover:underline cursor-pointer whitespace-nowrap"
                  >
                    Gerenciar todas →
                  </button>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead className="bg-slate-50 text-[#0B3D2E] border-b border-slate-200 text-left">
                      <tr>
                        <th className="py-2.5 px-4 font-semibold">Doador</th>
                        <th className="py-2.5 px-4 font-semibold">Categoria</th>
                        <th className="py-2.5 px-4 font-semibold text-right">Qtd.</th>
                        <th className="py-2.5 px-4 font-semibold">Data</th>
                        <th className="py-2.5 px-4 font-semibold">Descrição</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {ultimas5Doacoes.map((d) => (
                        <tr key={d.id} className="hover:bg-slate-50/90">
                          <td className="py-2.5 px-4 font-medium">{d.doador}</td>
                          <td className="py-2.5 px-4">
                            {CATEGORIAS_META[d.tipo].emoji} {CATEGORIAS_META[d.tipo].rotulo}
                          </td>
                          <td className="py-2.5 px-4 text-right font-mono tabular-nums font-semibold">
                            {d.quantidade}
                          </td>
                          <td className="py-2.5 px-4 font-mono tabular-nums text-[#4B635B]">
                            {formatarDataBR(d.data_doacao)}
                          </td>
                          <td className="py-2.5 px-4 text-[#4B635B]">{d.descricao || '—'}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </section>
            </div>
          )}

          {/* SCREEN 2: DOAÇÕES (CRUD) */}
          {screen === 'doacoes' && (
            <div className="space-y-5">
              <form
                onSubmit={handleSalvarDoacao}
                className="bg-white rounded-xl border border-[#D4AF37]/70 shadow-snow overflow-hidden"
              >
                <PiscaPiscaStrip count={14} compact />
                <div className="p-5 pt-2 space-y-4">
                  <div className="flex items-center justify-between">
                    <h2 className="font-christmas text-2xl font-bold text-[#0B3D2E]">
                      {editId ? `Editar Doação #${editId}` : 'Cadastrar Nova Doação'}
                    </h2>
                    {editId && (
                      <button
                        type="button"
                        onClick={limparFormularioDoacao}
                        className="text-xs text-[#C1272D] font-medium hover:underline cursor-pointer"
                      >
                        Cancelar edição
                      </button>
                    )}
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div>
                      <label className="block text-xs font-semibold mb-1">Nome do Doador *</label>
                      <input
                        type="text"
                        value={doador}
                        onChange={(e) => setDoador(e.target.value)}
                        placeholder="Ex.: Supermercado Estrela"
                        className="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm focus:outline-none focus:border-[#0B3D2E]"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold mb-1">Tipo de Item *</label>
                      <select
                        value={tipo}
                        onChange={(e) => setTipo(e.target.value as CategoriaTipo)}
                        className="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm bg-white focus:outline-none focus:border-[#0B3D2E]"
                      >
                        {(Object.keys(CATEGORIAS_META) as CategoriaTipo[]).map((k) => (
                          <option key={k} value={k}>
                            {CATEGORIAS_META[k].emoji} {CATEGORIAS_META[k].rotulo}
                          </option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <label className="block text-xs font-semibold mb-1">Quantidade *</label>
                      <input
                        type="number"
                        min={1}
                        value={quantidade}
                        onChange={(e) => setQuantidade(e.target.value)}
                        placeholder="Ex.: 10"
                        className="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm font-mono tabular-nums focus:outline-none focus:border-[#0B3D2E]"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold mb-1">Data da Doação *</label>
                      <input
                        type="date"
                        value={dataDoacao}
                        onChange={(e) => setDataDoacao(e.target.value)}
                        className="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm font-mono tabular-nums focus:outline-none focus:border-[#0B3D2E]"
                      />
                    </div>
                  </div>

                  <div className="flex flex-col lg:flex-row gap-4 items-end">
                    <div className="flex-1 w-full">
                      <label className="block text-xs font-semibold mb-1">Descrição Opcional</label>
                      <input
                        type="text"
                        value={descricao}
                        onChange={(e) => setDescricao(e.target.value)}
                        placeholder="Detalhes dos itens recebidos..."
                        className="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm focus:outline-none focus:border-[#0B3D2E]"
                      />
                    </div>
                    <div className="flex items-center gap-2.5 shrink-0">
                      <button
                        type="submit"
                        className="h-10 px-5 rounded-lg bg-[#0B3D2E] hover:bg-[#082C21] text-white text-sm font-semibold inline-flex items-center gap-2 transition-colors cursor-pointer whitespace-nowrap"
                      >
                        <Plus className="w-4 h-4" />
                        <span>{editId ? 'Atualizar' : 'Salvar Doação'}</span>
                      </button>
                      <button
                        type="button"
                        onClick={limparFormularioDoacao}
                        className="h-10 px-4 rounded-lg bg-slate-100 hover:bg-slate-200 text-[#122620] text-sm font-medium transition-colors cursor-pointer whitespace-nowrap"
                      >
                        Limpar
                      </button>
                    </div>
                  </div>
                </div>
              </form>

              <div className="bg-white rounded-xl p-4 border border-slate-200 shadow-snow flex flex-col sm:flex-row gap-3 items-center">
                <div className="relative flex-1 w-full">
                  <Search className="w-4 h-4 text-[#4B635B] absolute left-3 top-3" />
                  <input
                    type="text"
                    value={buscaDoador}
                    onChange={(e) => setBuscaDoador(e.target.value)}
                    placeholder="Buscar por nome do doador..."
                    className="w-full h-10 pl-9 pr-3 rounded-lg border border-slate-200 text-sm focus:outline-none focus:border-[#0B3D2E]"
                  />
                </div>
                <select
                  value={filtroTipo}
                  onChange={(e) => setFiltroTipo(e.target.value as 'todos' | CategoriaTipo)}
                  className="h-10 px-3 rounded-lg border border-slate-200 text-sm bg-white w-full sm:w-52"
                >
                  <option value="todos">Todos os tipos</option>
                  {(Object.keys(CATEGORIAS_META) as CategoriaTipo[]).map((k) => (
                    <option key={k} value={k}>
                      {CATEGORIAS_META[k].emoji} {CATEGORIAS_META[k].rotulo}
                    </option>
                  ))}
                </select>
              </div>

              <div className="bg-white rounded-xl border border-slate-200 shadow-snow overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead className="bg-slate-50 text-[#0B3D2E] border-b border-slate-200 text-left">
                      <tr>
                        <th className="py-2.5 px-4 font-semibold">ID</th>
                        <th className="py-2.5 px-4 font-semibold">Doador</th>
                        <th className="py-2.5 px-4 font-semibold">Categoria</th>
                        <th className="py-2.5 px-4 font-semibold text-right">Qtd.</th>
                        <th className="py-2.5 px-4 font-semibold">Data</th>
                        <th className="py-2.5 px-4 font-semibold">Descrição</th>
                        <th className="py-2.5 px-4 font-semibold text-right">Ações</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {doacoesFiltradas.length === 0 ? (
                        <tr>
                          <td colSpan={7} className="py-8 text-center text-[#4B635B]">
                            Nenhuma doação encontrada com os filtros atuais.
                          </td>
                        </tr>
                      ) : (
                        doacoesFiltradas.map((d) => (
                          <tr key={d.id} className="hover:bg-slate-50/90">
                            <td className="py-2.5 px-4 font-mono tabular-nums text-[#4B635B]">
                              #{d.id}
                            </td>
                            <td className="py-2.5 px-4 font-medium">{d.doador}</td>
                            <td className="py-2.5 px-4 whitespace-nowrap">
                              {CATEGORIAS_META[d.tipo].emoji} {CATEGORIAS_META[d.tipo].rotulo}
                            </td>
                            <td className="py-2.5 px-4 text-right font-mono tabular-nums font-semibold">
                              {d.quantidade}
                            </td>
                            <td className="py-2.5 px-4 font-mono tabular-nums text-[#4B635B]">
                              {formatarDataBR(d.data_doacao)}
                            </td>
                            <td className="py-2.5 px-4 text-[#4B635B]">{d.descricao || '—'}</td>
                            <td className="py-2.5 px-4 text-right whitespace-nowrap space-x-2">
                              <button
                                onClick={() => {
                                  setEditId(d.id);
                                  setDoador(d.doador);
                                  setTipo(d.tipo);
                                  setQuantidade(String(d.quantidade));
                                  setDataDoacao(d.data_doacao);
                                  setDescricao(d.descricao);
                                  window.scrollTo({ top: 0, behavior: 'smooth' });
                                }}
                                className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md bg-amber-50 text-[#9A7B16] hover:bg-amber-100 text-xs font-medium cursor-pointer"
                              >
                                <Edit3 className="w-3.5 h-3.5" />
                                Editar
                              </button>
                              <button
                                onClick={() => handleExcluirDoacao(d)}
                                className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md bg-red-50 text-[#C1272D] hover:bg-red-100 text-xs font-medium cursor-pointer"
                              >
                                <Trash2 className="w-3.5 h-3.5" />
                                Excluir
                              </button>
                            </td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* SCREEN 3: ESTOQUE (Cards de Itens com Pisca-Pisca) */}
          {screen === 'estoque' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
                {(Object.keys(CATEGORIAS_META) as CategoriaTipo[]).map((cat) => {
                  const qtd = estoque[cat];
                  const baixo = qtd < 5;
                  return (
                    <div
                      key={cat}
                      className={`rounded-xl border shadow-snow overflow-hidden transition-transform hover:-translate-y-0.5 ${
                        baixo
                          ? 'bg-[#FFF5F5] border-[#C1272D]'
                          : 'bg-white border-[#D4AF37]/80'
                      }`}
                    >
                      <PiscaPiscaStrip count={6} compact />
                      <div className="p-4 pt-2">
                        <div className="text-sm font-semibold text-[#0B3D2E] flex items-center gap-1.5">
                          <span>{CATEGORIAS_META[cat].emoji}</span>
                          <span>{CATEGORIAS_META[cat].rotulo}</span>
                        </div>
                        <div
                          className={`font-mono tabular-nums text-3xl font-bold mt-2 ${
                            baixo ? 'text-[#C1272D]' : 'text-[#122620]'
                          }`}
                        >
                          {qtd} <span className="text-sm font-normal">un.</span>
                        </div>
                        <div
                          className={`mt-2 text-xs font-medium flex items-center gap-1 ${
                            baixo ? 'text-[#C1272D]' : 'text-[#0B3D2E]'
                          }`}
                        >
                          {baixo ? (
                            <>
                              <AlertTriangle className="w-3.5 h-3.5" />
                              <span>Estoque baixo (&lt; 5)</span>
                            </>
                          ) : (
                            <>
                              <CheckCircle2 className="w-3.5 h-3.5" />
                              <span>Nível adequado</span>
                            </>
                          )}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>

              <div className="bg-white rounded-xl p-5 border border-[#D4AF37]/70 shadow-snow flex flex-col md:flex-row items-end gap-4">
                <div className="flex-1 w-full">
                  <label className="block text-xs font-semibold mb-1">
                    Categoria para Ajuste Manual
                  </label>
                  <select
                    value={ajusteTipo}
                    onChange={(e) => setAjusteTipo(e.target.value as CategoriaTipo)}
                    className="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm bg-white"
                  >
                    {(Object.keys(CATEGORIAS_META) as CategoriaTipo[]).map((k) => (
                      <option key={k} value={k}>
                        {CATEGORIAS_META[k].emoji} {CATEGORIAS_META[k].rotulo} (Atual: {estoque[k]}{' '}
                        un.)
                      </option>
                    ))}
                  </select>
                </div>
                <div className="w-full md:w-44">
                  <label className="block text-xs font-semibold mb-1">Quantidade</label>
                  <input
                    type="number"
                    min={1}
                    value={ajusteQtd}
                    onChange={(e) => setAjusteQtd(e.target.value)}
                    placeholder="Ex.: 5"
                    className="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm font-mono tabular-nums"
                  />
                </div>
                <div className="flex gap-2.5 shrink-0">
                  <button
                    onClick={() => handleAjusteEstoque(1)}
                    className="h-10 px-4 rounded-lg bg-[#0B3D2E] hover:bg-[#082C21] text-white text-sm font-semibold cursor-pointer whitespace-nowrap"
                  >
                    + Entrada
                  </button>
                  <button
                    onClick={() => handleAjusteEstoque(-1)}
                    className="h-10 px-4 rounded-lg bg-[#C1272D] hover:bg-[#9E1F24] text-white text-sm font-semibold cursor-pointer whitespace-nowrap"
                  >
                    - Saída
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* SCREEN 4: DISTRIBUIÇÕES */}
          {screen === 'distribuicoes' && (
            <div className="space-y-5">
              <form
                onSubmit={handleRegistrarDistribuicao}
                className="bg-white rounded-xl border border-[#D4AF37]/70 shadow-snow overflow-hidden"
              >
                <PiscaPiscaStrip count={14} compact />
                <div className="p-5 pt-2 space-y-4">
                  <h2 className="font-christmas text-2xl font-bold text-[#0B3D2E]">
                    ⭐ Registrar Entrega Solidária
                  </h2>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-xs font-semibold mb-1">Item do Estoque *</label>
                      <select
                        value={distTipo}
                        onChange={(e) => setDistTipo(e.target.value as CategoriaTipo)}
                        className="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm bg-white"
                      >
                        {(Object.keys(CATEGORIAS_META) as CategoriaTipo[]).map((k) => (
                          <option key={k} value={k}>
                            {CATEGORIAS_META[k].emoji} {CATEGORIAS_META[k].rotulo} ({estoque[k]}{' '}
                            disp.)
                          </option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <label className="block text-xs font-semibold mb-1">
                        Quantidade a Distribuir *
                      </label>
                      <input
                        type="number"
                        min={1}
                        value={distQtd}
                        onChange={(e) => setDistQtd(e.target.value)}
                        placeholder={`Máx.: ${estoque[distTipo]}`}
                        className="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm font-mono tabular-nums"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold mb-1">Data da Entrega *</label>
                      <input
                        type="date"
                        value={dataEntrega}
                        onChange={(e) => setDataEntrega(e.target.value)}
                        className="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm font-mono tabular-nums"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold mb-1">
                        Nome do Beneficiário *
                      </label>
                      <input
                        type="text"
                        value={beneficiario}
                        onChange={(e) => setBeneficiario(e.target.value)}
                        placeholder="Ex.: Abrigo Lar Feliz"
                        className="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold mb-1">
                        Responsável pela Entrega *
                      </label>
                      <input
                        type="text"
                        value={responsavel}
                        onChange={(e) => setResponsavel(e.target.value)}
                        placeholder="Ex.: Mariana Costa"
                        className="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm"
                      />
                    </div>
                    <div className="flex items-end">
                      <button
                        type="submit"
                        className="w-full h-10 px-5 rounded-lg bg-[#C1272D] hover:bg-[#9E1F24] text-white text-sm font-semibold transition-colors cursor-pointer whitespace-nowrap"
                      >
                        ⭐ Confirmar Distribuição
                      </button>
                    </div>
                  </div>
                </div>
              </form>

              <div className="bg-white rounded-xl p-4 border border-slate-200 shadow-snow relative">
                <Search className="w-4 h-4 text-[#4B635B] absolute left-7 top-7" />
                <input
                  type="text"
                  value={buscaBeneficiario}
                  onChange={(e) => setBuscaBeneficiario(e.target.value)}
                  placeholder="Buscar no histórico pelo nome do beneficiário..."
                  className="w-full h-10 pl-9 pr-3 rounded-lg border border-slate-200 text-sm"
                />
              </div>

              <div className="bg-white rounded-xl border border-slate-200 shadow-snow overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead className="bg-slate-50 text-[#0B3D2E] border-b border-slate-200 text-left">
                      <tr>
                        <th className="py-2.5 px-4 font-semibold">ID</th>
                        <th className="py-2.5 px-4 font-semibold">Item</th>
                        <th className="py-2.5 px-4 font-semibold text-right">Qtd.</th>
                        <th className="py-2.5 px-4 font-semibold">Beneficiário</th>
                        <th className="py-2.5 px-4 font-semibold">Data Entrega</th>
                        <th className="py-2.5 px-4 font-semibold">Responsável</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {distribuicoesFiltradas.map((d) => (
                        <tr key={d.id} className="hover:bg-slate-50/90">
                          <td className="py-2.5 px-4 font-mono tabular-nums text-[#4B635B]">
                            #{d.id}
                          </td>
                          <td className="py-2.5 px-4 whitespace-nowrap">
                            {CATEGORIAS_META[d.item_tipo].emoji}{' '}
                            {CATEGORIAS_META[d.item_tipo].rotulo}
                          </td>
                          <td className="py-2.5 px-4 text-right font-mono tabular-nums font-semibold">
                            {d.quantidade}
                          </td>
                          <td className="py-2.5 px-4 font-medium">{d.beneficiario}</td>
                          <td className="py-2.5 px-4 font-mono tabular-nums text-[#4B635B]">
                            {formatarDataBR(d.data_entrega)}
                          </td>
                          <td className="py-2.5 px-4 text-[#4B635B]">{d.responsavel}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* SCREEN 5: GRÁFICOS */}
          {screen === 'graficos' && (
            <div className="space-y-5">
              <div className="bg-white rounded-xl p-4 border border-[#D4AF37]/70 shadow-snow flex flex-wrap items-center justify-between gap-4 text-sm">
                <div className="font-semibold text-[#0B3D2E]">
                  📊 Indicador Arrecadado vs. Distribuído
                </div>
                <div className="flex flex-wrap items-center gap-4 font-mono tabular-nums">
                  <span>Arrecadado: {totalDoado} un.</span>
                  <span aria-hidden="true">·</span>
                  <span className="text-[#C1272D] font-semibold">
                    Distribuído: {totalDistribuido} un. ({taxaEntrega}%)
                  </span>
                  <span aria-hidden="true">·</span>
                  <span className="text-[#9A7B16] font-semibold">
                    Em estoque: {totalEstoque} un.
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
                <div className="bg-white rounded-xl border border-slate-200 shadow-snow overflow-hidden">
                  <PiscaPiscaStrip count={10} compact />
                  <div className="p-5 pt-2">
                    <h3 className="font-semibold text-[#0B3D2E] mb-4">
                      Doações Recebidas por Tipo de Item
                    </h3>
                    <div className="h-64">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={dadosPorCategoria}>
                          <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                          <XAxis dataKey="categoria" tick={{ fontSize: 12 }} />
                          <YAxis tick={{ fontSize: 12 }} />
                          <Tooltip />
                          <Bar dataKey="quantidade" radius={[6, 6, 0, 0]}>
                            {dadosPorCategoria.map((entry, idx) => (
                              <Cell key={idx} fill={entry.cor} />
                            ))}
                          </Bar>
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-xl border border-slate-200 shadow-snow overflow-hidden">
                  <PiscaPiscaStrip count={10} compact />
                  <div className="p-5 pt-2">
                    <h3 className="font-semibold text-[#0B3D2E] mb-4">
                      Distribuição Percentual por Categoria
                    </h3>
                    <div className="h-64">
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie
                            data={dadosPorCategoria}
                            dataKey="quantidade"
                            nameKey="categoria"
                            cx="50%"
                            cy="50%"
                            outerRadius={88}
                            label={({ name, percent }) =>
                              `${name} ${(Number(percent || 0) * 100).toFixed(0)}%`
                            }
                          >
                            {dadosPorCategoria.map((entry, idx) => (
                              <Cell key={idx} fill={entry.cor} />
                            ))}
                          </Pie>
                          <Tooltip />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-xl border border-slate-200 shadow-snow overflow-hidden lg:col-span-2">
                  <PiscaPiscaStrip count={18} compact />
                  <div className="p-5 pt-2">
                    <h3 className="font-semibold text-[#0B3D2E] mb-4">
                      Evolução das Doações (Últimos 30 Dias)
                    </h3>
                    <div className="h-64">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={dadosUltimos30Dias}>
                          <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                          <XAxis dataKey="dia" tick={{ fontSize: 11 }} interval={4} />
                          <YAxis tick={{ fontSize: 12 }} />
                          <Tooltip />
                          <Line
                            type="monotone"
                            dataKey="quantidade"
                            stroke="#C1272D"
                            strokeWidth={2.5}
                            dot={{ r: 3, fill: '#D4AF37', stroke: '#0B3D2E' }}
                          />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* SCREEN 6: SOBRE & PYTHON */}
          {screen === 'sobre' && (
            <div className="space-y-5">
              <div className="bg-white rounded-2xl border border-[#D4AF37]/80 shadow-snow overflow-hidden">
                <PiscaPiscaStrip count={16} compact />
                <div className="p-6 pt-3">
                  <h2 className="font-christmas text-3xl font-bold text-[#0B3D2E]">
                    🎄 Solidário Tech — Natal Branco · Tech Solutions 2026
                  </h2>
                  <p className="text-sm text-[#9A7B16] font-medium mt-1">
                    3º A – Técnico em Desenvolvimento de Sistemas · Sistema Desktop em Python
                  </p>
                  <p className="text-sm text-[#4B635B] mt-4 leading-relaxed max-w-3xl">
                    O código-fonte completo da aplicação desktop em Python está estruturado na pasta{' '}
                    <code className="bg-slate-100 px-1.5 py-0.5 rounded font-mono text-xs text-[#0B3D2E]">
                      solidario_tech/
                    </code>{' '}
                    com tema Natal Branco, luzes pisca-pisca nos cartões de itens, banco SQLite
                    pré-populado (
                    <code className="bg-slate-100 px-1.5 py-0.5 rounded font-mono text-xs text-[#0B3D2E]">
                      solidario_tech.db
                    </code>
                    ), gráficos Matplotlib/Seaborn + Pandas e ícones gerados via Pillow.
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-white rounded-xl border border-slate-200 shadow-snow overflow-hidden">
                  <PiscaPiscaStrip count={7} compact />
                  <div className="p-5 pt-2">
                    <h3 className="font-semibold text-[#0B3D2E]">💾 Banco de Dados</h3>
                    <p className="text-xs text-[#4B635B] mt-2 leading-relaxed">
                      SQLite 3 relacional com restrições CHECK, integridade referencial, seed
                      automático das 5 categorias e transações atômicas em{' '}
                      <span className="font-mono">database/connection.py</span>.
                    </p>
                  </div>
                </div>
                <div className="bg-white rounded-xl border border-slate-200 shadow-snow overflow-hidden">
                  <PiscaPiscaStrip count={7} compact />
                  <div className="p-5 pt-2">
                    <h3 className="font-semibold text-[#C1272D]">📊 Ciência de Dados</h3>
                    <p className="text-xs text-[#4B635B] mt-2 leading-relaxed">
                      Agregações por categoria e janela temporal de 30 dias com Pandas e gráficos
                      embutidos via <span className="font-mono">FigureCanvasTkAgg</span> em{' '}
                      <span className="font-mono">services/relatorio_service.py</span>.
                    </p>
                  </div>
                </div>
                <div className="bg-white rounded-xl border border-slate-200 shadow-snow overflow-hidden">
                  <PiscaPiscaStrip count={7} compact />
                  <div className="p-5 pt-2">
                    <h3 className="font-semibold text-[#9A7B16]">🛠️ Desenvolvimento (POO)</h3>
                    <p className="text-xs text-[#4B635B] mt-2 leading-relaxed">
                      Arquitetura em camadas (UI → Service → Repository → Model → SQLite), logs em{' '}
                      <span className="font-mono">app.log</span> e pop-ups natalinos personalizados.
                    </p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-snow">
                <h3 className="font-semibold text-[#0B3D2E] mb-2">
                  Como executar o aplicativo desktop Python localmente
                </h3>
                <pre className="bg-slate-900 text-emerald-100 rounded-lg p-4 text-xs font-mono overflow-x-auto leading-relaxed">
{`cd solidario_tech
pip install -r requirements.txt
python main.py`}
                </pre>
              </div>
            </div>
          )}
        </main>
      </div>

      {/* Festive Pop-up Modal */}
      {popup.open && (
        <div className="fixed inset-0 bg-slate-900/35 backdrop-blur-[1px] z-50 flex items-center justify-center p-4">
          <div
            className={`bg-white rounded-2xl max-w-md w-full border-2 shadow-xl animate-fade-in overflow-hidden ${
              popup.tipo === 'erro' ? 'border-[#C1272D]' : 'border-[#D4AF37]'
            }`}
          >
            <PiscaPiscaStrip count={9} compact />
            <div className="p-6 pt-3">
              <div className="flex items-start justify-between gap-3">
                <h3
                  className={`font-christmas text-2xl font-bold ${
                    popup.tipo === 'erro' ? 'text-[#C1272D]' : 'text-[#0B3D2E]'
                  }`}
                >
                  {popup.icone} {popup.titulo}
                </h3>
                <button
                  onClick={() => setPopup((p) => ({ ...p, open: false }))}
                  className="text-[#4B635B] hover:text-[#122620] cursor-pointer"
                  aria-label="Fechar"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              <p className="text-sm text-[#122620] mt-3 leading-relaxed">{popup.mensagem}</p>
              <div className="mt-5 flex justify-end">
                <button
                  onClick={() => setPopup((p) => ({ ...p, open: false }))}
                  className={`px-5 py-2 rounded-lg text-white text-sm font-semibold cursor-pointer ${
                    popup.tipo === 'erro'
                      ? 'bg-[#C1272D] hover:bg-[#9E1F24]'
                      : 'bg-[#0B3D2E] hover:bg-[#082C21]'
                  }`}
                >
                  Fechar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
