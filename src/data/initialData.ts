export type CategoriaTipo = 'brinquedo' | 'alimento' | 'roupa' | 'dinheiro' | 'cesta';

export interface DoacaoRecord {
  id: number;
  doador: string;
  tipo: CategoriaTipo;
  quantidade: number;
  data_doacao: string; // YYYY-MM-DD
  descricao: string;
}

export interface DistribuicaoRecord {
  id: number;
  doacao_id?: number;
  item_tipo: CategoriaTipo;
  quantidade: number;
  beneficiario: string;
  data_entrega: string; // YYYY-MM-DD
  responsavel: string;
}

export type EstoqueMap = Record<CategoriaTipo, number>;

export const CATEGORIAS_META: Record<
  CategoriaTipo,
  { emoji: string; rotulo: string; cor: string }
> = {
  brinquedo: { emoji: '🎁', rotulo: 'Brinquedo', cor: '#0B3D2E' },
  alimento: { emoji: '🍪', rotulo: 'Alimento', cor: '#C1272D' },
  roupa: { emoji: '🧥', rotulo: 'Roupa', cor: '#D4AF37' },
  dinheiro: { emoji: '💰', rotulo: 'Dinheiro', cor: '#1F6E56' },
  cesta: { emoji: '🧺', rotulo: 'Cesta básica', cor: '#8E1B20' },
};

export const FRASES_SOLIDARIEDADE: string[] = [
  'O melhor presente é aquele que aquece o coração.',
  'Pequenos gestos de solidariedade iluminam o Natal de muitas famílias.',
  'Doar é transformar carinho em esperança concreta.',
  'Quando compartilhamos, a magia do Natal se multiplica.',
  'Tecnologia e empatia unidas para cuidar de quem mais precisa.',
];

function diasAtras(n: number): string {
  const d = new Date();
  d.setDate(d.getDate() - n);
  return d.toISOString().slice(0, 10);
}

export function createInitialSeed(): {
  doacoes: DoacaoRecord[];
  distribuicoes: DistribuicaoRecord[];
  estoque: EstoqueMap;
} {
  const doacoes: DoacaoRecord[] = [
    { id: 1, doador: 'Supermercado Estrela do Sul', tipo: 'cesta', quantidade: 18, data_doacao: diasAtras(27), descricao: 'Cestas básicas natalinas com panetone' },
    { id: 2, doador: 'Colégio São José — Turma 3º A', tipo: 'brinquedo', quantidade: 32, data_doacao: diasAtras(24), descricao: 'Bonecas, carrinhos e jogos educativos' },
    { id: 3, doador: 'Padaria Bom Sabor', tipo: 'alimento', quantidade: 25, data_doacao: diasAtras(21), descricao: 'Panetones, biscoitos e achocolatados' },
    { id: 4, doador: 'Comunidade Vila Esperança', tipo: 'roupa', quantidade: 20, data_doacao: diasAtras(18), descricao: 'Agasalhos infantis e camisetas novas' },
    { id: 5, doador: 'Associação Comercial Local', tipo: 'dinheiro', quantidade: 15, data_doacao: diasAtras(15), descricao: 'Cotas de apoio financeiro (R$ 100 cada)' },
    { id: 6, doador: 'Família Andrade', tipo: 'brinquedo', quantidade: 14, data_doacao: diasAtras(12), descricao: 'Bolas de futebol e kits de desenho' },
    { id: 7, doador: 'Mercado Central Solidário', tipo: 'alimento', quantidade: 30, data_doacao: diasAtras(9), descricao: 'Arroz, feijão, óleo e macarrão' },
    { id: 8, doador: 'Loja Encanto Kids', tipo: 'roupa', quantidade: 16, data_doacao: diasAtras(7), descricao: 'Conjuntos infantis de verão' },
    { id: 9, doador: 'Empresa Tech Solutions', tipo: 'cesta', quantidade: 12, data_doacao: diasAtras(5), descricao: 'Cestas completas para famílias cadastradas' },
    { id: 10, doador: 'Grupo Voluntários do Bem', tipo: 'brinquedo', quantidade: 22, data_doacao: diasAtras(3), descricao: 'Brinquedos embrulhados para entrega' },
    { id: 11, doador: 'Dra. Camila Nogueira', tipo: 'dinheiro', quantidade: 8, data_doacao: diasAtras(2), descricao: 'Cotas destinadas à ceia comunitária' },
    { id: 12, doador: 'Igreja Matriz Santa Luzia', tipo: 'alimento', quantidade: 18, data_doacao: diasAtras(1), descricao: 'Kits de café da manhã e doces natalinos' },
  ];

  const distribuicoes: DistribuicaoRecord[] = [
    { id: 1, doacao_id: 9, item_tipo: 'cesta', quantidade: 26, beneficiario: 'Abrigo Lar Feliz', data_entrega: diasAtras(10), responsavel: 'Mariana Costa' },
    { id: 2, doacao_id: 10, item_tipo: 'brinquedo', quantidade: 38, beneficiario: 'Creche Pequeno Príncipe', data_entrega: diasAtras(6), responsavel: 'Lucas Ferreira' },
    { id: 3, doacao_id: 12, item_tipo: 'alimento', quantidade: 45, beneficiario: 'Cozinha Comunitária Esperança', data_entrega: diasAtras(4), responsavel: 'Ana Paula Silva' },
    { id: 4, doacao_id: 8, item_tipo: 'roupa', quantidade: 24, beneficiario: 'Projeto Mãos Unidas', data_entrega: diasAtras(3), responsavel: 'Rafael Oliveira' },
    { id: 5, doacao_id: 11, item_tipo: 'dinheiro', quantidade: 20, beneficiario: 'Casa de Apoio São Vicente', data_entrega: diasAtras(1), responsavel: 'Mariana Costa' },
  ];

  const estoque: EstoqueMap = {
    brinquedo: 30,
    alimento: 28,
    roupa: 12,
    dinheiro: 3,
    cesta: 4,
  };

  return { doacoes, distribuicoes, estoque };
}
