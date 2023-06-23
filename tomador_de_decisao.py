import numpy as np

class TomadorDeDecisao():
    def __getMaximoMinimo(self, matrizDecisao):
        #r^max_j = max(r_ij)
        rmax = np.max(matrizDecisao, axis=0)
        
        #r^min_j = min(r_ij)
        rmin = np.min(matrizDecisao, axis=0)
        
        return rmax, rmin

    def __getPertinencia(self, matrizDecisao, maxmin, rmax, rmin, pesos):
        pertinencia = np.zeros(matrizDecisao.shape)
        for i in range(matrizDecisao.shape[0]):
            for j in range(matrizDecisao.shape[1]):
                #maxmin: 0 é minimizacao; 1 é maximizacao
                if not (maxmin):
                    #A_ij(r_ij) = [(r_ij - r_j^min)/(r_j^max - r_j^min)], minimizacao
                    A_ij = (rmax[j] - matrizDecisao[i,j] ) / (rmax[j] - rmin[j])
                #A_ij(r_ij)^w_j
                pertinencia[i,j] = A_ij ** pesos[j]
        return pertinencia

    def __defNota(self, intersecao, pertinencia):
        #C_i = min(A_i1(r_i1),A_i2(r_i2),...,A_im(r_im))
        notas = np.zeros(pertinencia.shape[0])
        for i in range(pertinencia.shape[0]):
            if intersecao.lower() == 'min':
                notas[i] = np.min(pertinencia[i,:])
            else:
                raise Exception('Tipo de intersecao inexistente.')
        return notas

    def bellzadeh(self, _matrizDecisao, pesos, maxmin):
        matrizDecisao = np.asarray(_matrizDecisao)
        #Normalizar matriz
        matrizNormalizada = matrizDecisao / np.linalg.norm(matrizDecisao, ord=2, axis=0)
        
        #Definir T-norma
        intersecao = 'min'
        
        #Determinar valores maximos e minimos
        rmax, rmin = self.__getMaximoMinimo(matrizNormalizada)
        
        #Calcular pertinencia
        pertinencia = self.__getPertinencia(matrizNormalizada, maxmin, rmax, rmin, pesos)
        
        #Definir notas
        score = self.__defNota(intersecao, pertinencia)
        
        #Ordenar soluções
        ordem = np.argsort(score)[::-1]
        notas = score[ordem]
        elements = matrizDecisao[ordem]
        
        return elements, notas, ordem

    def topsis(self, _matrizDecisao, _pesos, _maxmin):
        matrizDecisao = np.asarray(_matrizDecisao)
        pesos = np.asarray(_pesos)
        maxmin = np.asarray(_maxmin)
        #Normalizar matriz
        matrizNormalizada = matrizDecisao / np.linalg.norm(matrizDecisao, ord=2, axis=0)

        #Calcular matriz ponderada
        matrizPonderada = matrizNormalizada * pesos

        #Identificar PIS e NIS
        PIS = np.max(matrizPonderada, axis=0) if maxmin else np.min(matrizPonderada, axis=0)
        NIS = np.min(matrizPonderada, axis=0) if maxmin else np.max(matrizPonderada, axis=0)

        #Calcular medidas de separação
        DPlus = np.linalg.norm(matrizPonderada - PIS, ord=2, axis=1)
        DLess = np.linalg.norm(matrizPonderada - NIS, ord=2, axis=1)

        #Definir proximidade relativa
        aux = DLess / (DPlus + DLess)

        #Ordenar soluções
        ordem = np.argsort(aux)[::-1]
        notas = aux[ordem]
        elements = matrizDecisao[ordem]

        return elements, notas, ordem

