import cv2
from ultralytics import YOLO
import numpy as np
import os
from datetime import datetime
from glob import glob 

ARQUIVO_DE_TESTE = 'IMG0000100.jpg' 
LARGURA_MAX_EXIBICAO = 1800 
ALTURA_MAX_EXIBICAO = 900 


class SistemaDetecaoFratura:
    def __init__(self, model_path, confidence_threshold=0.3, class_names=None): 
        try:
            full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', model_path)
            self.model = YOLO(full_path)
            print(f"✅ Modelo carregado com sucesso de: {full_path}")
            self.confidence_threshold = confidence_threshold
            if class_names is None:
                self.class_names = self.model.names
            else:
                self.class_names = class_names 
            if self.class_names is None or not self.class_names:
                self.class_names = {0: 'fracture'}
            print("📋 Classes do modelo:", self.class_names)
        except Exception as e:
            print(f"❌ Erro ao carregar modelo. Verifique o caminho e permissões: {e}")
            raise
    
    def analisar_raio_x(self, image_path, salvar_resultado=True):
        print(f"🔍 Analisando: {os.path.basename(image_path)}")
        if not os.path.exists(image_path):
            print(f"❌ Arquivo não encontrado: {image_path}")
            return None, None
        image = cv2.imread(image_path)
        if image is None:
            print("❌ Erro ao carregar imagem")
            return None, None
        
        # AQUI o modelo usa o novo self.confidence_threshold (0.3)
        results = self.model.predict(image, verbose=False, conf=self.confidence_threshold)
        
        dados_fratura = {
            'total_fraturas': 0,
            'localizacoes': [],
            'confiancas': [],
            'classes_detectadas': [],
            'nivel_severidade': 'Nenhuma fratura detectada',
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        image_with_boxes = results[0].plot()
        for result in results:
            if result.boxes is not None and len(result.boxes) > 0:
                for box in result.boxes:
                    confidence = float(box.conf[0])
                    class_id = int(box.cls[0])
                    class_name = self.class_names.get(class_id, 'Desconhecida')
                    dados_fratura['total_fraturas'] += 1
                    dados_fratura['confiancas'].append(confidence)
                    dados_fratura['classes_detectadas'].append(class_name)
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    dados_fratura['localizacoes'].append((x1, y1, x2, y2))
        
        # Chamada com o texto corrigido
        dados_fratura['nivel_severidade'] = self._determinar_severidade(dados_fratura['total_fraturas'])
        
        info_texto = [
            f"Fraturas: {dados_fratura['total_fraturas']}",
            f"Severidade: {dados_fratura['nivel_severidade']}",
        ]
        if dados_fratura['confiancas']:
            conf_media_texto = f"Confianca Media: {np.mean(dados_fratura['confiancas']):.2f}"
            info_texto.append(conf_media_texto)
        
        # Configurações para texto maior
        font_scale = 1.0
        thickness = 3

        for i, texto in enumerate(info_texto):
            cv2.putText(image_with_boxes, texto,
                        (20, 50 + i * 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        font_scale, 
                        (0, 255, 0), 
                        thickness)
        
        if salvar_resultado:
            os.makedirs('resultados', exist_ok=True)
            nome_arquivo = f"resultados/{os.path.splitext(os.path.basename(image_path))[0]}_resultado.jpg"
            cv2.imwrite(nome_arquivo, image_with_boxes)
            print(f"💾 Resultado salvo em: {nome_arquivo}")
        
        return image_with_boxes, dados_fratura
    
    def _determinar_severidade(self, total_fraturas):
        if total_fraturas == 0:
            return "Nenhuma fratura detectada"
        elif total_fraturas == 1:
            return "Fratura unica"
        elif total_fraturas <= 3:
            return "Multiplas fraturas (moderada)"
        else:
            return "Fraturas multiplas graves (alta)"
    
    def gerar_relatorio(self, dados_fratura, id_paciente="Desconhecido"):
        
        if dados_fratura['confiancas']:
            confianca_media = f"{np.mean(dados_fratura['confiancas']):.2f}"
        else:
            confianca_media = 'N/A'
            
        relatorio = f"""
{'='*60}
🏥 RELATORIO DE DIAGNOSTICO - DETECCAO DE FRATURAS
{'='*60}
📋 ID do Paciente: {id_paciente}
📅 Data/Hora: {dados_fratura['timestamp']}

📊 Resultados:
    • Total de fraturas detectadas: {dados_fratura['total_fraturas']}
    • Nivel de severidade: {dados_fratura['nivel_severidade']}
    • Confianca media: {confianca_media}  
    
🔍 Detalhes:
"""
        if dados_fratura['total_fraturas'] > 0:
            for i, (classe, confianca) in enumerate(zip(dados_fratura['classes_detectadas'],
                                                        dados_fratura['confiancas']), 1):
                relatorio += f"   {i}. {classe} - Confianca: {confianca:.2f}\n"
        else:
            relatorio += "   ✅ Nenhuma fratura detectada\n"
        
        relatorio += """
💡 Recomendacoes:
    • Consultar ortopedista para avaliacao detalhada.
    • Resultados devem ser validados por profissional.
"""
        return relatorio

def main():
    print("🚀 SISTEMA DE DETECCAO DE FRATURAS - TESTE RAPIDO")
    print("=" * 55)
    
    model_path_relative_to_root = 'model/fracture_fracatlas/best.pt'
    
    full_model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', model_path_relative_to_root)
    if not os.path.exists(full_model_path):
        print(f"❌ Erro Critico: Modelo nao encontrado. Por favor, coloque 'best.pt' em: \n\n    {os.path.join('model', 'fracture_fracatlas')}\n")
        return
    
    detector = SistemaDetecaoFratura(model_path_relative_to_root)
    
    images_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'images')
    caminho_completo_arquivo = os.path.join(images_dir, ARQUIVO_DE_TESTE)
    
    if not os.path.exists(caminho_completo_arquivo):
        print(f"\n❌ Erro: Arquivo '{ARQUIVO_DE_TESTE}' nao encontrado.")
        print(f"Certifique-se de que ele esta na pasta: {images_dir}")
        return
    
    print(f"\n🎯 Analisando arquivo: {ARQUIVO_DE_TESTE}")
    
    is_image = ARQUIVO_DE_TESTE.lower().endswith(('.jpg', '.jpeg', '.png'))

    if is_image:
        imagem_com_boxes_e_texto, dados_fratura = detector.analisar_raio_x(caminho_completo_arquivo, salvar_resultado=True)
        
        if imagem_com_boxes_e_texto is not None:
            
            imagem_para_exibir = imagem_com_boxes_e_texto.copy()
            
            altura_original, largura_original = imagem_para_exibir.shape[:2]
            
            if largura_original > LARGURA_MAX_EXIBICAO or altura_original > ALTURA_MAX_EXIBICAO:
                
                fator_largura = LARGURA_MAX_EXIBICAO / largura_original
                fator_altura = ALTURA_MAX_EXIBICAO / altura_original
                
                fator_redimensionamento = min(fator_largura, fator_altura)
                
                nova_largura = int(largura_original * fator_redimensionamento)
                nova_altura = int(altura_original * fator_redimensionamento)
                
                imagem_para_exibir = cv2.resize(imagem_para_exibir, (nova_largura, nova_altura))
            
            relatorio = detector.gerar_relatorio(dados_fratura, os.path.basename(caminho_completo_arquivo))
            print(relatorio)
            cv2.imshow(f"Resultado - {ARQUIVO_DE_TESTE}", imagem_para_exibir)
            cv2.waitKey(0) 
            cv2.destroyAllWindows() 
        else:
            print("⚠️ Aviso: Nao foi possivel realizar a analise da imagem.")
    
    else:
        results = detector.model.predict(caminho_completo_arquivo, 
                                        save=True, 
                                        project='resultados', 
                                        name=f'{os.path.splitext(ARQUIVO_DE_TESTE)[0]}_analise', 
                                        conf=detector.confidence_threshold)
        
        print("\n=======================================================")
        print("✅ Analise concluida.")
        print(f"O resultado da analise do video foi salvo em: resultados\\{os.path.splitext(ARQUIVO_DE_TESTE)[0]}_analise\\")
        print("Verifique o arquivo .avi ou .mp4 dentro desta pasta.")


if __name__ == "__main__":

    main()
