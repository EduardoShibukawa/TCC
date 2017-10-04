unit Model.Noticia;

interface

type
  TSentimento = (senNegativo, senPositivo);
  TNoticia = class
  private
    FSentimento: TSentimento;
    FTitulo: String;
    FConteudo: String;
    FDataAtualizacao: TDateTime;
    procedure SetConteudo(const Value: String);
    procedure SetDataAtualizacao(const Value: TDateTime);
    procedure SetSentimento(const Value: TSentimento);
    procedure SetTitulo(const Value: String);
  published
    property DataAtualizacao: TDateTime read FDataAtualizacao write SetDataAtualizacao;
    property Titulo: String read FTitulo write SetTitulo;
    property Conteudo: String read FConteudo write SetConteudo;
    property Sentimento: TSentimento read FSentimento write SetSentimento;
  end;

implementation

{ TNoticia }

procedure TNoticia.SetConteudo(const Value: String);
begin
  FConteudo := Value;
end;

procedure TNoticia.SetDataAtualizacao(const Value: TDateTime);
begin
  FDataAtualizacao := Value;
end;

procedure TNoticia.SetSentimento(const Value: TSentimento);
begin
  FSentimento := Value;
end;

procedure TNoticia.SetTitulo(const Value: String);
begin
  FTitulo := Value;
end;

end.
