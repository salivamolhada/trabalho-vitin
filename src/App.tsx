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
  { left: '4%', size: '14px', duration: '15s', delay: '0s', drift: '20px', opacity: 0.55 },
  { left: '13%', size: '17px', duration: '19s', delay: '-4s', drift: '-24px', opacity: 0.45 },
  { left: '23%', size: '12px', duration: '14s', delay: '-8s', drift: '18px', opacity: 0.6 },
  { left: '36%', size: '15px', duration: '21s', delay: '-2s', drift: '-18px', opacity: 0.4 },
  { left: '49%', size: '13px', duration: '16s', delay: '-6s', drift: '26px', opacity: 0.55 },
  { left: '62%', size: '18px', duration: '22s', delay: '-11s', drift: '-22px', opacity: 0.42 },
  { left: '75%', size: '12px', duration: '15s', delay: '-3s', drift: '16px', opacity: 0.58 },
  { left: '86%', size: '15px', duration: '18s', delay: '-9s', drift: '-20px', opacity: 0.48 },
  { left: '94%', size: '11px', duration: '13s', delay: '-5s', drift: '14px', opacity: 0.5 },
];

const BULB_PALETTE = [
  { main: '#FF3B5C', dark: '#990F2B' },
  { main: '#FFD43B', dark: '#B47B00' },
  { main: '#22E58A', dark: '#0B7A47' },
  { main: '#38BDF8', dark: '#0B6B9B' },
  { main: '#C084FC', dark: '#6B21A8' },
  { main: '#FB923C', dark: '#B44309' },
];

// Paleta 3D colorida para as 5 categorias de itens
const CATEGORIA_3D_STYLE: Record<
  CategoriaTipo,
  { grad: string; border: string; chartColor: string }
> = {
  brinquedo: {
    grad: 'bg-gradient-to-br from-[#126E52] via-[#0D543E] to-[#083829]',
    border: 'border-[#34D399]/50',
    chartColor: '#34D399',
  },
  alimento: {
    grad: 'bg-gradient-to-br from-[#D93843] via-[#B41E28] to-[#7D1119]',
    border: 'border-[#FDA4AF]/50',
    chartColor: '#FB7185',
  },
  roupa: {
    grad: 'bg-gradient-to-br from-[#2563EB] via-[#1D4ED8] to-[#1E3A8A]',
    border: 'border-[#93C5FD]/50',
    chartColor: '#60A5FA',
  },
  dinheiro: {
    grad: 'bg-gradient-to-br from-[#D97706] via-[#B45309] to-[#78350F]',
    border: 'border-[#FCD34D]/60',
    chartColor: '#FBBF24',
  },
  cesta: {
    grad: 'bg-gradient-to-br from-[#9333EA] via-[#7E22CE] to-[#4C1D95]',
    border: 'border-[#D8B4FE]/50',
    chartColor: '#C084FC',
  },
};

function formatarDataBR(iso: string): string {
  const parts = iso.slice(0, 10).split('-');
  if (parts.length !== 3) return iso;
  return `${parts[2]}/${parts[1]}/${parts[0]}`;
}

function PineGiftLogo() {
  return (
    <svg width="44" height="44" viewBox="0 0 64 64" fill="none" aria-hidden="true">
      <defs>
        <radialGradient id="logoBg3d" cx="35%" cy="30%" r="70%">
          <stop offset="0%" stopColor="#B91C1C" />
          <stop offset="100%" stopColor="#450A0A" />
        </radialGradient>
        <linearGradient id="pine3d" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#34D399" />
          <stop offset="100%" stopColor="#065F46" />
        </linearGradient>
      </defs>
      <circle cx="32" cy="32" r="30" fill="url(#logoBg3d)" stroke="#F5C451" strokeWidth="2.5" />
      <polygon points="32,8 34.5,13.5 40,13.5 35.5,17 37,22.5 32,19 27,22.5 28.5,17 24,13.5 29.5,13.5" fill="#FDE047" />
      <polygon points="32,16 18,32 46,32" fill="url(#pine3d)" />
      <polygon points="32,24 14,42 50,42" fill="url(#pine3d)" />
      <rect x="29" y="42" width="6" height="6" fill="#78350F" />
      <rect x="23" y="45" width="18" height="12" rx="2" fill="#EF4444" stroke="#FDE047" strokeWidth="1.2" />
      <rect x="30.5" y="45" width="3" height="12" fill="#FDE047" />
      <rect x="23" y="49.5" width="18" height="3" fill="#FDE047" />
    </svg>
  );
}

/** Ramo decorativo colorido 3D de Natal */
function HollyCornerAccent() {
  return (
    <svg width="50" height="34" viewBox="0 0 48 32" fill="none" aria-hidden="true" className="shrink-0">
      <path d="M6 22C13 13 22 9 34 11C28 19 19 24 6 22Z" fill="#10B981" />
      <path d="M18 24C24 17 33 16 43 20C34 26 25 27 18 24Z" fill="#059669" />
      <circle cx="19" cy="18" r="3.4" fill="#FF3B5C" />
      <circle cx="18" cy="17" r="1" fill="#FFD1DC" />
      <circle cx="24.5" cy="14.5" r="2.9" fill="#EF4444" />
      <circle cx="24" cy="21.5" r="2.8" fill="#F59E0B" />
      <circle cx="38" cy="10" r="2" fill="#FDE047" />
    </svg>
  );
}

/** Papai Noel e 3 reninhas coloridas com sombreamento 3D voando no fundo da pagina */
function SantaSleighArtwork({ scale = 1 }: { scale?: number }) {
  return (
    <svg
      width={Math.round(350 * scale)}
      height={Math.round(118 * scale)}
      viewBox="0 0 350 118"
      fill="none"
      aria-hidden="true"
    >
      <defs>
        <linearGradient id="sleighBody3d" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#FF4D6D" />
          <stop offset="55%" stopColor="#C9184A" />
          <stop offset="100%" stopColor="#720922" />
        </linearGradient>
        <linearGradient id="gold3d" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#FEF08A" />
          <stop offset="50%" stopColor="#F59E0B" />
          <stop offset="100%" stopColor="#B45309" />
        </linearGradient>
        <radialGradient id="reindeer3d" cx="35%" cy="30%" r="70%">
          <stop offset="0%" stopColor="#D98A52" />
          <stop offset="65%" stopColor="#9C572C" />
          <stop offset="100%" stopColor="#5C2D12" />
        </radialGradient>
        <radialGradient id="rudolphBody3d" cx="35%" cy="30%" r="70%">
          <stop offset="0%" stopColor="#E59866" />
          <stop offset="65%" stopColor="#A0522D" />
          <stop offset="100%" stopColor="#642E14" />
        </radialGradient>
      </defs>

      {/* Poeira estelar colorida 3D */}
      <circle cx="14" cy="70" r="2.6" fill="#FDE047" />
      <circle cx="28" cy="58" r="2" fill="#38BDF8" />
      <circle cx="38" cy="76" r="2.4" fill="#34D399" />
      <polygon points="48,46 50,51 55,51 51,54 52.5,59 48,56 43.5,59 45,54 41,51 46,51" fill="#FDE047" />

      {/* Patins dourados 3D do treno */}
      <path
        d="M54 86 C68 96, 122 96, 138 82 M64 87 L68 74 M116 87 L112 74"
        stroke="url(#gold3d)"
        strokeWidth="3.8"
        strokeLinecap="round"
      />
      {/* Corpo 3D do treno */}
      <path
        d="M56 54 C56 72, 74 79, 122 77 L132 56 C118 63, 102 63, 90 56 L56 54 Z"
        fill="url(#sleighBody3d)"
        stroke="#FDE047"
        strokeWidth="1.8"
      />
      {/* Presentes coloridos 3D no treno */}
      <ellipse cx="75" cy="51" rx="14" ry="12" fill="#059669" />
      <rect x="64" y="34" width="12" height="10" rx="2" fill="#38BDF8" stroke="#FEF08A" strokeWidth="1" transform="rotate(-12 64 34)" />
      <rect x="78" y="36" width="11" height="10" rx="2" fill="#A855F7" stroke="#FEF08A" strokeWidth="1" transform="rotate(10 78 36)" />
      <rect x="71" y="42" width="10" height="9" rx="2" fill="#F59E0B" stroke="#FFFFFF" strokeWidth="1" />

      {/* Papai Noel 3D */}
      <circle cx="102" cy="49" r="10" fill="#EF4444" stroke="#FEF08A" strokeWidth="1" />
      <circle cx="102" cy="36" r="6.5" fill="#FFE0BD" />
      <path d="M95.5 38 C98 46, 106 46, 108.5 38 Z" fill="#FFFFFF" />
      <path d="M94.5 33 L102 20 L109.5 33 Z" fill="#EF4444" />
      <rect x="94.5" y="31.5" width="15" height="3.2" rx="1.6" fill="#FFFFFF" />
      <circle cx="102" cy="20" r="2.6" fill="#FFFFFF" />
      <path d="M108 46 L119 34" stroke="#EF4444" strokeWidth="4.4" strokeLinecap="round" />
      <circle cx="120" cy="33" r="2.5" fill="#FFFFFF" />

      {/* Redeas douradas brilhantes */}
      <path d="M124 58 Q170 66, 294 56" stroke="#FDE047" strokeWidth="1.6" strokeDasharray="4 2" />
      <path d="M126 62 Q180 71, 240 60" stroke="#F59E0B" strokeWidth="1.4" />

      {/* Reninha 1 */}
      <g transform="translate(164, 38)">
        <ellipse cx="22" cy="24" rx="15" ry="8" fill="url(#reindeer3d)" />
        <path d="M30 20 L39 10" stroke="#A65E32" strokeWidth="6" strokeLinecap="round" />
        <circle cx="41" cy="9.5" r="5" fill="url(#reindeer3d)" />
        {/* Cachecol festivo verde */}
        <path d="M29 19 Q34 22 37 16" stroke="#10B981" strokeWidth="3.2" strokeLinecap="round" />
        <path d="M29 20 L21 24" stroke="#34D399" strokeWidth="2.4" strokeLinecap="round" />
        <path d="M39 5 L37 -1 M39 2 L42 0 M43 5 L46 -1" stroke="#FDE047" strokeWidth="1.6" strokeLinecap="round" />
        <path d="M12 29 L5 40 M18 30 L16 42 M28 30 L34 40 M33 29 L41 37" stroke="#854822" strokeWidth="2.6" strokeLinecap="round" />
        <circle cx="34" cy="18" r="2.4" fill="#FDE047" />
      </g>

      {/* Reninha 2 */}
      <g transform="translate(220, 31)">
        <ellipse cx="22" cy="24" rx="15" ry="8" fill="url(#reindeer3d)" />
        <path d="M30 20 L39 10" stroke="#B26739" strokeWidth="6" strokeLinecap="round" />
        <circle cx="41" cy="9.5" r="5" fill="url(#reindeer3d)" />
        {/* Cachecol festivo azul/dourado */}
        <path d="M29 19 Q34 22 37 16" stroke="#38BDF8" strokeWidth="3.2" strokeLinecap="round" />
        <path d="M29 20 L21 24" stroke="#7DD3FC" strokeWidth="2.4" strokeLinecap="round" />
        <path d="M39 5 L37 -1 M39 2 L42 0 M43 5 L46 -1" stroke="#FDE047" strokeWidth="1.6" strokeLinecap="round" />
        <path d="M12 29 L5 40 M18 30 L16 42 M28 30 L34 40 M33 29 L41 37" stroke="#854822" strokeWidth="2.6" strokeLinecap="round" />
        <circle cx="34" cy="18" r="2.4" fill="#FDE047" />
      </g>

      {/* Reninha 3 (Rudolph liderando com nariz 3D brilhante) */}
      <g transform="translate(278, 24)">
        <ellipse cx="22" cy="24" rx="15.5" ry="8.4" fill="url(#rudolphBody3d)" />
        <path d="M30 20 L40 10" stroke="#B56537" strokeWidth="6.2" strokeLinecap="round" />
        <circle cx="42" cy="9.5" r="5.2" fill="url(#rudolphBody3d)" />
        {/* Cachecol festivo vermelho & ouro */}
        <path d="M29 19 Q35 22 38 16" stroke="#EF4444" strokeWidth="3.4" strokeLinecap="round" />
        <path d="M29 20 L20 25" stroke="#FDE047" strokeWidth="2.4" strokeLinecap="round" />
        <path d="M39 5 L37 -2 M39 2 L42 -1 M43 5 L47 -2" stroke="#FDE047" strokeWidth="1.7" strokeLinecap="round" />
        <path d="M12 29 L4 40 M18 30 L16 42 M28 30 L35 40 M33 29 L42 36" stroke="#7C411D" strokeWidth="2.7" strokeLinecap="round" />
        <circle cx="35" cy="18" r="2.5" fill="#FDE047" />
        <circle cx="48" cy="9.5" r="3.4" fill="#FF2E4D" className="rudolph-glow" />
        <circle cx="47" cy="8.5" r="1" fill="#FFFFFF" />
      </g>
    </svg>
  );
}

/** Cordao curvo de pisca-pisca 3D colorido */
function PiscaPiscaStrip({
  count = 9,
  compact = false,
}: {
  count?: number;
  compact?: boolean;
}) {
  return (
    <div
      className={`relative flex items-start justify-between w-full overflow-hidden select-none pointer-events-none ${
        compact ? 'px-3 pt-1 pb-1.5' : 'px-5 pt-1.5 pb-2'
      }`}
      aria-hidden="true"
    >
      <svg
        className="absolute inset-x-0 top-0 w-full h-4"
        viewBox="0 0 400 16"
        preserveAspectRatio="none"
      >
        <path
          d="M0,4 Q50,13 100,4 T200,4 T300,4 T400,4"
          fill="none"
          stroke="#F5C451"
          strokeOpacity="0.55"
          strokeWidth="1.6"
        />
      </svg>

      {Array.from({ length: count }).map((_, idx) => {
        const bulb = BULB_PALETTE[idx % BULB_PALETTE.length];
        const delay = `${((idx % 4) * 0.28).toFixed(2)}s`;
        const duration = `${(1.1 + (idx % 3) * 0.26).toFixed(2)}s`;
        const dropOffset = idx % 2 === 0 ? 'mt-0.5' : 'mt-1.5';
        return (
          <span key={idx} className={`relative z-10 flex flex-col items-center ${dropOffset}`}>
            <span className="w-1.5 h-1.5 bg-[#0B3D2E] border border-[#F5C451]/60 rounded-t-xs" />
            <span
              className={`pisca-bulb-3d rounded-full ${compact ? 'w-3 h-3.5' : 'w-3.5 h-4'}`}
              style={
                {
                  background: `radial-gradient(circle at 35% 28%, #FFFFFF 0%, ${bulb.main} 45%, ${bulb.dark} 100%)`,
                  color: bulb.main,
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
      cor: CATEGORIA_3D_STYLE[k].chartColor,
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
    dashboard: 'Painel Inicial — Natal Solidário',
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

  const taxaEntregaNum = totalDoado > 0 ? Math.min(100, (totalDistribuido / totalDoado) * 100) : 0;
  const taxaEntrega = taxaEntregaNum.toFixed(1);

  return (
    <div className={`min-h-screen text-[#FFF9F0] flex relative ${luzesAtivas ? '' : 'pisca-paused'}`}>
      {/* Fundo Natalino Vermelho: Neve dourada + Reninhas e Papai Noel 3D voando */}
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

        {/* Reninhas e Papai Noel voando no céu vermelho */}
        <div className="santa-sleigh-fly">
          <SantaSleighArtwork scale={1.12} />
        </div>

        <div className="santa-sleigh-fly-secondary">
          <SantaSleighArtwork scale={0.82} />
        </div>
      </div>

      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/55 backdrop-blur-xs z-30 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Left Sidebar — Veludo Vermelho Natalino com detalhes em Ouro e Verde */}
      <aside
        className={`fixed lg:static inset-y-0 left-0 z-40 w-64 bg-gradient-to-b from-[#4F080D]/95 via-[#680E14]/95 to-[#3D0509]/95 backdrop-blur-md border-r border-[#F5C451]/35 flex flex-col justify-between transition-transform duration-200 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        <div>
          <div className="px-5 py-5 flex items-center gap-3 border-b border-[#F5C451]/25">
            <PineGiftLogo />
            <div>
              <div className="font-christmas text-2xl font-bold leading-none text-[#FFF9F0]">
                Solidário Tech
              </div>
              <div className="text-xs text-[#FDE047] font-medium mt-1">Campanha de Natal</div>
            </div>
          </div>

          <PiscaPiscaStrip count={7} compact />

          <nav className="p-3 space-y-1.5" aria-label="Navegação principal">
            {navItems.map((item) => {
              const ativo = screen === item.key;
              return (
                <button
                  key={item.key}
                  onClick={() => {
                    setScreen(item.key);
                    setSidebarOpen(false);
                  }}
                  className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-semibold transition-all whitespace-nowrap shrink-0 cursor-pointer ${
                    ativo
                      ? 'bg-gradient-to-r from-[#F5C451] via-[#FDE047] to-[#D99B1E] text-[#3B0609] btn-3d'
                      : 'text-[#FFE8D6] hover:bg-white/10 hover:text-white'
                  }`}
                >
                  {item.icon}
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>
        </div>

        <div className="p-4 m-3 rounded-xl bg-gradient-to-br from-[#0F513B] to-[#083526] border border-[#F5C451]/50 text-xs text-emerald-100 space-y-2 card-3d">
          <div className="font-semibold text-[#FDE047]">Desafio Tech Solutions 2026</div>
          <div>3º A · Técnico em Desenvolvimento de Sistemas</div>
          <button
            onClick={handleResetarDemo}
            className="w-full mt-1 flex items-center justify-center gap-1.5 py-2 px-2.5 rounded-lg bg-gradient-to-b from-[#D93843] to-[#9E141D] text-white font-semibold cursor-pointer whitespace-nowrap btn-3d"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Restaurar Seed</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0 relative z-10">
        {/* Top Bar Vermelho Rubi com Pisca-Pisca 3D */}
        <header className="bg-gradient-to-r from-[#4E080D]/90 via-[#6E1017]/90 to-[#4E080D]/90 backdrop-blur-md border-b border-[#F5C451]/35 shrink-0">
          <PiscaPiscaStrip count={20} />
          <div className="h-14 px-4 lg:px-8 flex items-center justify-between gap-4">
            <div className="flex items-center gap-3 min-w-0">
              <button
                onClick={() => setSidebarOpen(true)}
                className="lg:hidden p-2 rounded-lg border border-[#F5C451]/40 text-[#FDE047] bg-[#3B0509] cursor-pointer"
                aria-label="Abrir menu"
              >
                <Menu className="w-5 h-5" />
              </button>
              <h1 className="font-christmas text-2xl lg:text-3xl font-bold text-[#FFF9F0] truncate drop-shadow-sm">
                {titulos[screen]}
              </h1>
            </div>

            <div className="flex items-center gap-3 shrink-0">
              <button
                onClick={() => setLuzesAtivas((v) => !v)}
                className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold cursor-pointer whitespace-nowrap btn-3d ${
                  luzesAtivas
                    ? 'bg-gradient-to-b from-[#F5C451] to-[#D4971C] text-[#3B0609]'
                    : 'bg-[#3D060A] text-[#FFE4D6] border border-white/20'
                }`}
              >
                <Sparkles className="w-3.5 h-3.5" />
                <span>{luzesAtivas ? 'Pisca-pisca ativo' : 'Luzes pausadas'}</span>
              </button>

              <span className="hidden sm:inline-flex items-center gap-1.5 text-xs lg:text-sm text-[#FFE9B3] font-mono tabular-nums whitespace-nowrap">
                <Calendar className="w-4 h-4 text-[#FDE047]" />
                {hojeFormatado}
              </span>
            </div>
          </div>
        </header>

        <main className="flex-1 p-4 lg:p-7 max-w-[1320px] w-full mx-auto space-y-6 animate-fade-in">
          {/* SCREEN 1: DASHBOARD */}
          {screen === 'dashboard' && (
            <div className="space-y-6">
              {/* Banner Vermelho 3D com Pisca-Pisca e Ações Rápidas */}
              <section className="bg-gradient-to-br from-[#9E1922]/92 via-[#7A1017]/92 to-[#53090E]/92 backdrop-blur-sm rounded-2xl border border-[#F5C451]/60 card-3d overflow-hidden">
                <PiscaPiscaStrip count={16} compact />
                <div className="px-6 py-5 flex flex-col lg:flex-row lg:items-center justify-between gap-5">
                  <div className="space-y-2 max-w-2xl">
                    <div className="flex items-center gap-2.5">
                      <HollyCornerAccent />
                      <h2 className="font-christmas text-3xl lg:text-4xl font-bold text-[#FFF9F0] drop-shadow">
                        🎄 Feliz Natal! Que a solidariedade transforme vidas.
                      </h2>
                    </div>
                    <p className="text-sm text-[#FFE9B3] italic pl-1">
                      ⭐ &ldquo;{FRASES_SOLIDARIEDADE[fraseIdx]}&rdquo;
                    </p>
                    <div className="pt-1 flex items-center gap-3 text-xs text-[#FFF9F0]">
                      <span className="font-semibold text-[#FDE047]">
                        Progresso das entregas:
                      </span>
                      <div className="w-44 h-2.5 bg-[#3A0508] rounded-full overflow-hidden border border-[#F5C451]/40">
                        <div
                          className="h-full bg-gradient-to-r from-[#34D399] via-[#FDE047] to-[#38BDF8] transition-all duration-300"
                          style={{ width: `${taxaEntregaNum}%` }}
                        />
                      </div>
                      <span className="font-mono tabular-nums font-bold text-[#FDE047]">
                        {taxaEntrega}% entregue
                      </span>
                    </div>
                  </div>

                  <div className="flex flex-wrap items-center gap-3 shrink-0">
                    <button
                      onClick={() => setScreen('doacoes')}
                      className="h-10 px-4 rounded-xl bg-gradient-to-b from-[#168A65] to-[#0B533C] text-white text-sm font-semibold inline-flex items-center gap-2 cursor-pointer whitespace-nowrap btn-3d"
                    >
                      <Gift className="w-4 h-4 text-[#FDE047]" />
                      <span>+ Nova Doação</span>
                    </button>
                    <button
                      onClick={() => setScreen('distribuicoes')}
                      className="h-10 px-4 rounded-xl bg-gradient-to-b from-[#F5C451] to-[#D4971C] text-[#3B0609] text-sm font-bold inline-flex items-center gap-2 cursor-pointer whitespace-nowrap btn-3d"
                    >
                      <HeartHandshake className="w-4 h-4" />
                      <span>Registrar Entrega</span>
                    </button>
                  </div>
                </div>
              </section>

              {/* Cards 3D Coloridos de Resumo */}
              <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-gradient-to-br from-[#127053] via-[#0B4F3A] to-[#073325] rounded-2xl border border-[#34D399]/45 card-3d card-3d-hover overflow-hidden">
                  <PiscaPiscaStrip count={7} compact />
                  <div className="p-5 pt-2">
                    <div className="text-xs font-semibold text-emerald-100">
                      🎁 Total de Doações Recebidas
                    </div>
                    <div className="font-mono tabular-nums text-3xl font-bold text-white mt-1 drop-shadow">
                      {totalDoado} <span className="text-base font-normal text-emerald-200">un.</span>
                    </div>
                    <div className="text-xs text-emerald-200/90 mt-2">
                      {doacoes.length} registros cadastrados
                    </div>
                  </div>
                </div>

                <div className="bg-gradient-to-br from-[#C82333] via-[#9E1420] to-[#6B0A12] rounded-2xl border border-[#FDA4AF]/45 card-3d card-3d-hover overflow-hidden">
                  <PiscaPiscaStrip count={7} compact />
                  <div className="p-5 pt-2">
                    <div className="text-xs font-semibold text-rose-100">⭐ Total Distribuído</div>
                    <div className="font-mono tabular-nums text-3xl font-bold text-white mt-1 drop-shadow">
                      {totalDistribuido}{' '}
                      <span className="text-base font-normal text-rose-200">un.</span>
                    </div>
                    <div className="text-xs text-rose-100/90 mt-2">
                      {distribuicoes.length} entregas realizadas · {taxaEntrega}% do total
                    </div>
                  </div>
                </div>

                <div className="bg-gradient-to-br from-[#D98218] via-[#B45E09] to-[#783A04] rounded-2xl border border-[#FDE047]/55 card-3d card-3d-hover overflow-hidden">
                  <PiscaPiscaStrip count={7} compact />
                  <div className="p-5 pt-2">
                    <div className="text-xs font-semibold text-amber-100">🎄 Itens em Estoque</div>
                    <div className="font-mono tabular-nums text-3xl font-bold text-white mt-1 drop-shadow">
                      {totalEstoque}{' '}
                      <span className="text-base font-normal text-amber-100">un.</span>
                    </div>
                    <div className="text-xs mt-2 font-semibold text-[#FEF08A]">
                      {categoriasBaixas.length > 0
                        ? `⚠️ ${categoriasBaixas.length} categoria(s) abaixo de 5 un.`
                        : 'Todas as categorias em nível adequado'}
                    </div>
                  </div>
                </div>
              </section>

              {/* Mini-cards 3D super coloridos das 5 categorias */}
              <section className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3.5">
                {(Object.keys(CATEGORIAS_META) as CategoriaTipo[]).map((cat) => {
                  const qtd = estoque[cat];
                  const baixo = qtd < 5;
                  const style3d = CATEGORIA_3D_STYLE[cat];
                  return (
                    <button
                      key={cat}
                      onClick={() => setScreen('estoque')}
                      className={`text-left rounded-2xl border card-3d card-3d-hover overflow-hidden cursor-pointer ${style3d.grad} ${
                        baixo ? 'border-[#FF6B81] ring-2 ring-[#FF3B5C]/60' : style3d.border
                      }`}
                    >
                      <PiscaPiscaStrip count={5} compact />
                      <div className="px-4 pb-3.5 pt-1">
                        <div className="text-xs font-semibold text-white/95 flex items-center gap-1.5">
                          <span>{CATEGORIAS_META[cat].emoji}</span>
                          <span>{CATEGORIAS_META[cat].rotulo}</span>
                        </div>
                        <div className="font-mono tabular-nums text-2xl font-bold mt-1 text-white drop-shadow">
                          {qtd} un.
                        </div>
                        {baixo && (
                          <div className="text-[11px] font-semibold text-[#FFE4E6] mt-0.5">
                            ⚠️ Estoque baixo
                          </div>
                        )}
                      </div>
                    </button>
                  );
                })}
              </section>

              {/* Tabela Últimas 5 Doações em Rubi 3D */}
              <section className="bg-[#560B10]/90 backdrop-blur-sm rounded-2xl border border-[#F5C451]/45 card-3d overflow-hidden">
                <div className="px-5 py-4 border-b border-[#F5C451]/25 flex items-center justify-between">
                  <h3 className="font-semibold text-[#FDE047]">
                    🎁 Últimos 5 Registros de Doação
                  </h3>
                  <button
                    onClick={() => setScreen('doacoes')}
                    className="text-xs font-semibold text-[#FFE9B3] hover:text-white hover:underline cursor-pointer whitespace-nowrap"
                  >
                    Gerenciar todas →
                  </button>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead className="bg-[#3E060A] text-[#FDE047] border-b border-[#F5C451]/25 text-left">
                      <tr>
                        <th className="py-2.5 px-4 font-semibold">Doador</th>
                        <th className="py-2.5 px-4 font-semibold">Categoria</th>
                        <th className="py-2.5 px-4 font-semibold text-right">Qtd.</th>
                        <th className="py-2.5 px-4 font-semibold">Data</th>
                        <th className="py-2.5 px-4 font-semibold">Descrição</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-white/10">
                      {ultimas5Doacoes.map((d) => (
                        <tr key={d.id} className="hover:bg-white/5">
                          <td className="py-2.5 px-4 font-medium text-white">{d.doador}</td>
                          <td className="py-2.5 px-4 text-[#FFE9B3]">
                            {CATEGORIAS_META[d.tipo].emoji} {CATEGORIAS_META[d.tipo].rotulo}
                          </td>
                          <td className="py-2.5 px-4 text-right font-mono tabular-nums font-bold text-[#34D399]">
                            {d.quantidade}
                          </td>
                          <td className="py-2.5 px-4 font-mono tabular-nums text-rose-100/80">
                            {formatarDataBR(d.data_doacao)}
                          </td>
                          <td className="py-2.5 px-4 text-rose-100/80">{d.descricao || '—'}</td>
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
                className="bg-gradient-to-br from-[#6D1017]/95 to-[#48070C]/95 backdrop-blur-sm rounded-2xl border border-[#F5C451]/55 card-3d overflow-hidden"
              >
                <PiscaPiscaStrip count={14} compact />
                <div className="p-5 pt-2 space-y-4">
                  <div className="flex items-center justify-between">
                    <h2 className="font-christmas text-2xl font-bold text-[#FDE047]">
                      {editId ? `Editar Doação #${editId}` : 'Cadastrar Nova Doação'}
                    </h2>
                    {editId && (
                      <button
                        type="button"
                        onClick={limparFormularioDoacao}
                        className="text-xs text-[#FDA4AF] font-medium hover:underline cursor-pointer"
                      >
                        Cancelar edição
                      </button>
                    )}
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div>
                      <label className="block text-xs font-semibold text-[#FFE9B3] mb-1">
                        Nome do Doador *
                      </label>
                      <input
                        type="text"
                        value={doador}
                        onChange={(e) => setDoador(e.target.value)}
                        placeholder="Ex.: Supermercado Estrela"
                        className="w-full h-10 px-3 rounded-lg border border-[#F5C451]/40 text-sm text-white placeholder-rose-200/50 bg-[#360508] focus:outline-none focus:border-[#FDE047]"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-[#FFE9B3] mb-1">
                        Tipo de Item *
                      </label>
                      <select
                        value={tipo}
                        onChange={(e) => setTipo(e.target.value as CategoriaTipo)}
                        className="w-full h-10 px-3 rounded-lg border border-[#F5C451]/40 text-sm text-white bg-[#360508] focus:outline-none focus:border-[#FDE047]"
                      >
                        {(Object.keys(CATEGORIAS_META) as CategoriaTipo[]).map((k) => (
                          <option key={k} value={k}>
                            {CATEGORIAS_META[k].emoji} {CATEGORIAS_META[k].rotulo}
                          </option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-[#FFE9B3] mb-1">
                        Quantidade *
                      </label>
                      <input
                        type="number"
                        min={1}
                        value={quantidade}
                        onChange={(e) => setQuantidade(e.target.value)}
                        placeholder="Ex.: 10"
                        className="w-full h-10 px-3 rounded-lg border border-[#F5C451]/40 text-sm text-white placeholder-rose-200/50 font-mono tabular-nums bg-[#360508] focus:outline-none focus:border-[#FDE047]"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-[#FFE9B3] mb-1">
                        Data da Doação *
                      </label>
                      <input
                        type="date"
                        value={dataDoacao}
                        onChange={(e) => setDataDoacao(e.target.value)}
                        className="w-full h-10 px-3 rounded-lg border border-[#F5C451]/40 text-sm text-white font-mono tabular-nums bg-[#360508] focus:outline-none focus:border-[#FDE047]"
                      />
                    </div>
                  </div>

                  <div className="flex flex-col lg:flex-row gap-4 items-end">
                    <div className="flex-1 w-full">
                      <label className="block text-xs font-semibold text-[#FFE9B3] mb-1">
                        Descrição Opcional
                      </label>
                      <input
                        type="text"
                        value={descricao}
                        onChange={(e) => setDescricao(e.target.value)}
                        placeholder="Detalhes dos itens recebidos..."
                        className="w-full h-10 px-3 rounded-lg border border-[#F5C451]/40 text-sm text-white placeholder-rose-200/50 bg-[#360508] focus:outline-none focus:border-[#FDE047]"
                      />
                    </div>
                    <div className="flex items-center gap-2.5 shrink-0">
                      <button
                        type="submit"
                        className="h-10 px-5 rounded-xl bg-gradient-to-b from-[#168A65] to-[#0B533C] text-white text-sm font-semibold inline-flex items-center gap-2 cursor-pointer whitespace-nowrap btn-3d"
                      >
                        <Plus className="w-4 h-4" />
                        <span>{editId ? 'Atualizar' : 'Salvar Doação'}</span>
                      </button>
                      <button
                        type="button"
                        onClick={limparFormularioDoacao}
                        className="h-10 px-4 rounded-xl bg-[#3B0609] border border-white/20 hover:bg-[#520A0F] text-[#FFF9F0] text-sm font-medium cursor-pointer whitespace-nowrap btn-3d"
                      >
                        Limpar
                      </button>
                    </div>
                  </div>
                </div>
              </form>

              <div className="bg-[#560B10]/90 backdrop-blur-sm rounded-xl p-4 border border-[#F5C451]/35 card-3d flex flex-col sm:flex-row gap-3 items-center">
                <div className="relative flex-1 w-full">
                  <Search className="w-4 h-4 text-[#FDE047] absolute left-3 top-3" />
                  <input
                    type="text"
                    value={buscaDoador}
                    onChange={(e) => setBuscaDoador(e.target.value)}
                    placeholder="Buscar por nome do doador..."
                    className="w-full h-10 pl-9 pr-3 rounded-lg border border-[#F5C451]/35 text-sm text-white placeholder-rose-200/50 bg-[#360508] focus:outline-none focus:border-[#FDE047]"
                  />
                </div>
                <select
                  value={filtroTipo}
                  onChange={(e) => setFiltroTipo(e.target.value as 'todos' | CategoriaTipo)}
                  className="h-10 px-3 rounded-lg border border-[#F5C451]/35 text-sm text-white bg-[#360508] w-full sm:w-52"
                >
                  <option value="todos">Todos os tipos</option>
                  {(Object.keys(CATEGORIAS_META) as CategoriaTipo[]).map((k) => (
                    <option key={k} value={k}>
                      {CATEGORIAS_META[k].emoji} {CATEGORIAS_META[k].rotulo}
                    </option>
                  ))}
                </select>
              </div>

              <div className="bg-[#560B10]/90 backdrop-blur-sm rounded-2xl border border-[#F5C451]/45 card-3d overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead className="bg-[#3E060A] text-[#FDE047] border-b border-[#F5C451]/25 text-left">
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
                    <tbody className="divide-y divide-white/10">
                      {doacoesFiltradas.length === 0 ? (
                        <tr>
                          <td colSpan={7} className="py-8 text-center text-rose-100/80">
                            Nenhuma doação encontrada com os filtros atuais.
                          </td>
                        </tr>
                      ) : (
                        doacoesFiltradas.map((d) => (
                          <tr key={d.id} className="hover:bg-white/5">
                            <td className="py-2.5 px-4 font-mono tabular-nums text-[#FDE047]">
                              #{d.id}
                            </td>
                            <td className="py-2.5 px-4 font-medium text-white">{d.doador}</td>
                            <td className="py-2.5 px-4 whitespace-nowrap text-[#FFE9B3]">
                              {CATEGORIAS_META[d.tipo].emoji} {CATEGORIAS_META[d.tipo].rotulo}
                            </td>
                            <td className="py-2.5 px-4 text-right font-mono tabular-nums font-bold text-[#34D399]">
                              {d.quantidade}
                            </td>
                            <td className="py-2.5 px-4 font-mono tabular-nums text-rose-100/80">
                              {formatarDataBR(d.data_doacao)}
                            </td>
                            <td className="py-2.5 px-4 text-rose-100/80">{d.descricao || '—'}</td>
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
                                className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-gradient-to-b from-[#F5C451] to-[#D4971C] text-[#3B0609] text-xs font-bold cursor-pointer btn-3d"
                              >
                                <Edit3 className="w-3.5 h-3.5" />
                                Editar
                              </button>
                              <button
                                onClick={() => handleExcluirDoacao(d)}
                                className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-gradient-to-b from-[#EF4444] to-[#B91C1C] text-white text-xs font-bold cursor-pointer btn-3d"
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

          {/* SCREEN 3: ESTOQUE (Cards 3D super coloridos) */}
          {screen === 'estoque' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
                {(Object.keys(CATEGORIAS_META) as CategoriaTipo[]).map((cat) => {
                  const qtd = estoque[cat];
                  const baixo = qtd < 5;
                  const style3d = CATEGORIA_3D_STYLE[cat];
                  return (
                    <div
                      key={cat}
                      className={`rounded-2xl border card-3d card-3d-hover overflow-hidden ${style3d.grad} ${
                        baixo ? 'border-[#FF6B81] ring-2 ring-[#FF3B5C]/70' : style3d.border
                      }`}
                    >
                      <PiscaPiscaStrip count={6} compact />
                      <div className="p-4 pt-2">
                        <div className="text-sm font-semibold text-white flex items-center gap-1.5">
                          <span>{CATEGORIAS_META[cat].emoji}</span>
                          <span>{CATEGORIAS_META[cat].rotulo}</span>
                        </div>
                        <div className="font-mono tabular-nums text-3xl font-bold mt-2 text-white drop-shadow">
                          {qtd} <span className="text-sm font-normal text-white/80">un.</span>
                        </div>
                        <div
                          className={`mt-2 text-xs font-semibold flex items-center gap-1 ${
                            baixo ? 'text-[#FFE4E6]' : 'text-[#D1FAE5]'
                          }`}
                        >
                          {baixo ? (
                            <>
                              <AlertTriangle className="w-3.5 h-3.5 text-[#FDE047]" />
                              <span>Estoque baixo (&lt; 5)</span>
                            </>
                          ) : (
                            <>
                              <CheckCircle2 className="w-3.5 h-3.5 text-[#34D399]" />
                              <span>Nível adequado</span>
                            </>
                          )}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>

              <div className="bg-gradient-to-br from-[#6D1017]/95 to-[#48070C]/95 backdrop-blur-sm rounded-2xl p-5 border border-[#F5C451]/55 card-3d flex flex-col md:flex-row items-end gap-4">
                <div className="flex-1 w-full">
                  <label className="block text-xs font-semibold text-[#FFE9B3] mb-1">
                    Categoria para Ajuste Manual
                  </label>
                  <select
                    value={ajusteTipo}
                    onChange={(e) => setAjusteTipo(e.target.value as CategoriaTipo)}
                    className="w-full h-10 px-3 rounded-lg border border-[#F5C451]/40 text-sm text-white bg-[#360508]"
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
                  <label className="block text-xs font-semibold text-[#FFE9B3] mb-1">
                    Quantidade
                  </label>
                  <input
                    type="number"
                    min={1}
                    value={ajusteQtd}
                    onChange={(e) => setAjusteQtd(e.target.value)}
                    placeholder="Ex.: 5"
                    className="w-full h-10 px-3 rounded-lg border border-[#F5C451]/40 text-sm text-white placeholder-rose-200/50 font-mono tabular-nums bg-[#360508]"
                  />
                </div>
                <div className="flex gap-2.5 shrink-0">
                  <button
                    onClick={() => handleAjusteEstoque(1)}
                    className="h-10 px-4 rounded-xl bg-gradient-to-b from-[#168A65] to-[#0B533C] text-white text-sm font-semibold cursor-pointer whitespace-nowrap btn-3d"
                  >
                    + Entrada
                  </button>
                  <button
                    onClick={() => handleAjusteEstoque(-1)}
                    className="h-10 px-4 rounded-xl bg-gradient-to-b from-[#EF4444] to-[#B91C1C] text-white text-sm font-semibold cursor-pointer whitespace-nowrap btn-3d"
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
                className="bg-gradient-to-br from-[#6D1017]/95 to-[#48070C]/95 backdrop-blur-sm rounded-2xl border border-[#F5C451]/55 card-3d overflow-hidden"
              >
                <PiscaPiscaStrip count={14} compact />
                <div className="p-5 pt-2 space-y-4">
                  <h2 className="font-christmas text-2xl font-bold text-[#FDE047]">
                    ⭐ Registrar Entrega Solidária
                  </h2>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-xs font-semibold text-[#FFE9B3] mb-1">
                        Item do Estoque *
                      </label>
                      <select
                        value={distTipo}
                        onChange={(e) => setDistTipo(e.target.value as CategoriaTipo)}
                        className="w-full h-10 px-3 rounded-lg border border-[#F5C451]/40 text-sm text-white bg-[#360508]"
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
                      <label className="block text-xs font-semibold text-[#FFE9B3] mb-1">
                        Quantidade a Distribuir *
                      </label>
                      <input
                        type="number"
                        min={1}
                        value={distQtd}
                        onChange={(e) => setDistQtd(e.target.value)}
                        placeholder={`Máx.: ${estoque[distTipo]}`}
                        className="w-full h-10 px-3 rounded-lg border border-[#F5C451]/40 text-sm text-white placeholder-rose-200/50 font-mono tabular-nums bg-[#360508]"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-[#FFE9B3] mb-1">
                        Data da Entrega *
                      </label>
                      <input
                        type="date"
                        value={dataEntrega}
                        onChange={(e) => setDataEntrega(e.target.value)}
                        className="w-full h-10 px-3 rounded-lg border border-[#F5C451]/40 text-sm text-white font-mono tabular-nums bg-[#360508]"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-[#FFE9B3] mb-1">
                        Nome do Beneficiário *
                      </label>
                      <input
                        type="text"
                        value={beneficiario}
                        onChange={(e) => setBeneficiario(e.target.value)}
                        placeholder="Ex.: Abrigo Lar Feliz"
                        className="w-full h-10 px-3 rounded-lg border border-[#F5C451]/40 text-sm text-white placeholder-rose-200/50 bg-[#360508]"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-[#FFE9B3] mb-1">
                        Responsável pela Entrega *
                      </label>
                      <input
                        type="text"
                        value={responsavel}
                        onChange={(e) => setResponsavel(e.target.value)}
                        placeholder="Ex.: Mariana Costa"
                        className="w-full h-10 px-3 rounded-lg border border-[#F5C451]/40 text-sm text-white placeholder-rose-200/50 bg-[#360508]"
                      />
                    </div>
                    <div className="flex items-end">
                      <button
                        type="submit"
                        className="w-full h-10 px-5 rounded-xl bg-gradient-to-b from-[#F5C451] to-[#D4971C] text-[#3B0609] text-sm font-bold cursor-pointer whitespace-nowrap btn-3d"
                      >
                        ⭐ Confirmar Distribuição
                      </button>
                    </div>
                  </div>
                </div>
              </form>

              <div className="bg-[#560B10]/90 backdrop-blur-sm rounded-xl p-4 border border-[#F5C451]/35 card-3d relative">
                <Search className="w-4 h-4 text-[#FDE047] absolute left-7 top-7" />
                <input
                  type="text"
                  value={buscaBeneficiario}
                  onChange={(e) => setBuscaBeneficiario(e.target.value)}
                  placeholder="Buscar no histórico pelo nome do beneficiário..."
                  className="w-full h-10 pl-9 pr-3 rounded-lg border border-[#F5C451]/35 text-sm text-white placeholder-rose-200/50 bg-[#360508]"
                />
              </div>

              <div className="bg-[#560B10]/90 backdrop-blur-sm rounded-2xl border border-[#F5C451]/45 card-3d overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead className="bg-[#3E060A] text-[#FDE047] border-b border-[#F5C451]/25 text-left">
                      <tr>
                        <th className="py-2.5 px-4 font-semibold">ID</th>
                        <th className="py-2.5 px-4 font-semibold">Item</th>
                        <th className="py-2.5 px-4 font-semibold text-right">Qtd.</th>
                        <th className="py-2.5 px-4 font-semibold">Beneficiário</th>
                        <th className="py-2.5 px-4 font-semibold">Data Entrega</th>
                        <th className="py-2.5 px-4 font-semibold">Responsável</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-white/10">
                      {distribuicoesFiltradas.map((d) => (
                        <tr key={d.id} className="hover:bg-white/5">
                          <td className="py-2.5 px-4 font-mono tabular-nums text-[#FDE047]">
                            #{d.id}
                          </td>
                          <td className="py-2.5 px-4 whitespace-nowrap text-[#FFE9B3]">
                            {CATEGORIAS_META[d.item_tipo].emoji}{' '}
                            {CATEGORIAS_META[d.item_tipo].rotulo}
                          </td>
                          <td className="py-2.5 px-4 text-right font-mono tabular-nums font-bold text-[#34D399]">
                            {d.quantidade}
                          </td>
                          <td className="py-2.5 px-4 font-medium text-white">{d.beneficiario}</td>
                          <td className="py-2.5 px-4 font-mono tabular-nums text-rose-100/80">
                            {formatarDataBR(d.data_entrega)}
                          </td>
                          <td className="py-2.5 px-4 text-rose-100/80">{d.responsavel}</td>
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
              <div className="bg-gradient-to-r from-[#6D1017]/95 to-[#48070C]/95 backdrop-blur-sm rounded-2xl p-4 border border-[#F5C451]/55 card-3d flex flex-wrap items-center justify-between gap-4 text-sm">
                <div className="font-semibold text-[#FDE047]">
                  📊 Indicador Arrecadado vs. Distribuído
                </div>
                <div className="flex flex-wrap items-center gap-4 font-mono tabular-nums">
                  <span className="text-[#34D399] font-semibold">
                    Arrecadado: {totalDoado} un.
                  </span>
                  <span aria-hidden="true">·</span>
                  <span className="text-[#FDA4AF] font-semibold">
                    Distribuído: {totalDistribuido} un. ({taxaEntrega}%)
                  </span>
                  <span aria-hidden="true">·</span>
                  <span className="text-[#FDE047] font-semibold">
                    Em estoque: {totalEstoque} un.
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
                <div className="bg-[#560B10]/92 backdrop-blur-sm rounded-2xl border border-[#F5C451]/45 card-3d overflow-hidden">
                  <PiscaPiscaStrip count={10} compact />
                  <div className="p-5 pt-2">
                    <h3 className="font-semibold text-[#FDE047] mb-4">
                      Doações Recebidas por Tipo de Item
                    </h3>
                    <div className="h-64">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={dadosPorCategoria}>
                          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.14)" />
                          <XAxis dataKey="categoria" tick={{ fontSize: 12, fill: '#FFE9B3' }} />
                          <YAxis tick={{ fontSize: 12, fill: '#FFE9B3' }} />
                          <Tooltip
                            contentStyle={{
                              backgroundColor: '#3B0609',
                              borderColor: '#F5C451',
                              color: '#FFF9F0',
                              borderRadius: '10px',
                            }}
                          />
                          <Bar dataKey="quantidade" radius={[8, 8, 0, 0]}>
                            {dadosPorCategoria.map((entry, idx) => (
                              <Cell key={idx} fill={entry.cor} />
                            ))}
                          </Bar>
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>

                <div className="bg-[#560B10]/92 backdrop-blur-sm rounded-2xl border border-[#F5C451]/45 card-3d overflow-hidden">
                  <PiscaPiscaStrip count={10} compact />
                  <div className="p-5 pt-2">
                    <h3 className="font-semibold text-[#FDE047] mb-4">
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
                          <Tooltip
                            contentStyle={{
                              backgroundColor: '#3B0609',
                              borderColor: '#F5C451',
                              color: '#FFF9F0',
                              borderRadius: '10px',
                            }}
                          />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>

                <div className="bg-[#560B10]/92 backdrop-blur-sm rounded-2xl border border-[#F5C451]/45 card-3d overflow-hidden lg:col-span-2">
                  <PiscaPiscaStrip count={18} compact />
                  <div className="p-5 pt-2">
                    <h3 className="font-semibold text-[#FDE047] mb-4">
                      Evolução das Doações (Últimos 30 Dias)
                    </h3>
                    <div className="h-64">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={dadosUltimos30Dias}>
                          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.14)" />
                          <XAxis
                            dataKey="dia"
                            tick={{ fontSize: 11, fill: '#FFE9B3' }}
                            interval={4}
                          />
                          <YAxis tick={{ fontSize: 12, fill: '#FFE9B3' }} />
                          <Tooltip
                            contentStyle={{
                              backgroundColor: '#3B0609',
                              borderColor: '#F5C451',
                              color: '#FFF9F0',
                              borderRadius: '10px',
                            }}
                          />
                          <Line
                            type="monotone"
                            dataKey="quantidade"
                            stroke="#FDE047"
                            strokeWidth={3}
                            dot={{ r: 3.5, fill: '#34D399', stroke: '#FFF9F0' }}
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
              <div className="bg-gradient-to-br from-[#8E141D]/95 to-[#51090E]/95 backdrop-blur-sm rounded-2xl border border-[#F5C451]/60 card-3d overflow-hidden">
                <PiscaPiscaStrip count={16} compact />
                <div className="p-6 pt-3">
                  <h2 className="font-christmas text-3xl font-bold text-[#FFF9F0]">
                    🎄 Solidário Tech — Campanha de Natal · Tech Solutions 2026
                  </h2>
                  <p className="text-sm text-[#FDE047] font-medium mt-1">
                    3º A – Técnico em Desenvolvimento de Sistemas · Sistema Desktop em Python
                  </p>
                  <p className="text-sm text-[#FFE8D6] mt-4 leading-relaxed max-w-3xl">
                    O código-fonte completo da aplicação desktop em Python está estruturado na pasta{' '}
                    <code className="bg-[#360508] px-1.5 py-0.5 rounded font-mono text-xs text-[#FDE047]">
                      solidario_tech/
                    </code>{' '}
                    com visual natalino em vermelho vibrante, luzes pisca-pisca 3D nos cartões de
                    itens, banco SQLite pré-populado (
                    <code className="bg-[#360508] px-1.5 py-0.5 rounded font-mono text-xs text-[#FDE047]">
                      solidario_tech.db
                    </code>
                    ), gráficos Matplotlib/Seaborn + Pandas e ícones gerados via Pillow.
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-gradient-to-br from-[#127053] to-[#073325] rounded-2xl border border-[#34D399]/50 card-3d overflow-hidden">
                  <PiscaPiscaStrip count={7} compact />
                  <div className="p-5 pt-2">
                    <h3 className="font-semibold text-[#FDE047]">💾 Banco de Dados</h3>
                    <p className="text-xs text-emerald-100 mt-2 leading-relaxed">
                      SQLite 3 relacional com restrições CHECK, integridade referencial, seed
                      automático das 5 categorias e transações atômicas em{' '}
                      <span className="font-mono">database/connection.py</span>.
                    </p>
                  </div>
                </div>
                <div className="bg-gradient-to-br from-[#C82333] to-[#6B0A12] rounded-2xl border border-[#FDA4AF]/50 card-3d overflow-hidden">
                  <PiscaPiscaStrip count={7} compact />
                  <div className="p-5 pt-2">
                    <h3 className="font-semibold text-[#FDE047]">📊 Ciência de Dados</h3>
                    <p className="text-xs text-rose-100 mt-2 leading-relaxed">
                      Agregações por categoria e janela temporal de 30 dias com Pandas e gráficos
                      embutidos via <span className="font-mono">FigureCanvasTkAgg</span> em{' '}
                      <span className="font-mono">services/relatorio_service.py</span>.
                    </p>
                  </div>
                </div>
                <div className="bg-gradient-to-br from-[#2563EB] to-[#1E3A8A] rounded-2xl border border-[#93C5FD]/50 card-3d overflow-hidden">
                  <PiscaPiscaStrip count={7} compact />
                  <div className="p-5 pt-2">
                    <h3 className="font-semibold text-[#FDE047]">🛠️ Desenvolvimento (POO)</h3>
                    <p className="text-xs text-blue-100 mt-2 leading-relaxed">
                      Arquitetura em camadas (UI → Service → Repository → Model → SQLite), logs em{' '}
                      <span className="font-mono">app.log</span> e pop-ups natalinos personalizados.
                    </p>
                  </div>
                </div>
              </div>

              <div className="bg-[#560B10]/92 backdrop-blur-sm rounded-2xl p-5 border border-[#F5C451]/45 card-3d">
                <h3 className="font-semibold text-[#FDE047] mb-2">
                  Como executar o aplicativo desktop Python localmente
                </h3>
                <pre className="bg-[#2B0407] border border-[#F5C451]/25 text-[#A7F3D0] rounded-xl p-4 text-xs font-mono overflow-x-auto leading-relaxed">
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
        <div className="fixed inset-0 bg-black/60 backdrop-blur-xs z-50 flex items-center justify-center p-4">
          <div
            className={`bg-gradient-to-b from-[#6B0E15] to-[#44060A] text-[#FFF9F0] rounded-2xl max-w-md w-full border-2 card-3d animate-fade-in overflow-hidden ${
              popup.tipo === 'erro' ? 'border-[#FF6B81]' : 'border-[#F5C451]'
            }`}
          >
            <PiscaPiscaStrip count={9} compact />
            <div className="p-6 pt-3">
              <div className="flex items-start justify-between gap-3">
                <h3
                  className={`font-christmas text-2xl font-bold ${
                    popup.tipo === 'erro' ? 'text-[#FDA4AF]' : 'text-[#FDE047]'
                  }`}
                >
                  {popup.icone} {popup.titulo}
                </h3>
                <button
                  onClick={() => setPopup((p) => ({ ...p, open: false }))}
                  className="text-rose-200 hover:text-white cursor-pointer"
                  aria-label="Fechar"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              <p className="text-sm text-[#FFF9F0] mt-3 leading-relaxed">{popup.mensagem}</p>
              <div className="mt-5 flex justify-end">
                <button
                  onClick={() => setPopup((p) => ({ ...p, open: false }))}
                  className={`px-5 py-2 rounded-xl text-sm font-bold cursor-pointer btn-3d ${
                    popup.tipo === 'erro'
                      ? 'bg-gradient-to-b from-[#EF4444] to-[#B91C1C] text-white'
                      : 'bg-gradient-to-b from-[#F5C451] to-[#D4971C] text-[#3B0609]'
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
