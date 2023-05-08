class Restrictions():
    def capacidade(n, m, x, m_recursos_necessarios, v_capacidade_max):
        m_recursos_utilizados = m_recursos_necessarios.multiply(x,axis=0)
        for agente in range(n):
            custo_total = m_recursos_utilizados.iloc[agente].sum()
            if v_capacidade_max[agente] < custo_total:
                return False
