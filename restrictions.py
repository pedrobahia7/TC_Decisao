def capacidade_excedida(x, m_recursos_necessarios, v_capacidade_max):
    m_recursos_utilizados = m_recursos_necessarios.multiply(x,axis=0)
    for agente in range(len(x)):
        recursos_utilizados = m_recursos_utilizados.iloc[agente].sum()
        if recursos_utilizados > v_capacidade_max.iloc[agente].values[0]:
            return True
    return False
