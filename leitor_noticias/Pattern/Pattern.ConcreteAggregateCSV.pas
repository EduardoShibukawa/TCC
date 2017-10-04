unit Pattern.ConcreteAggregateCSV;

interface

uses
  Pattern.Iterator, Pattern.Aggregate, Contnrs, System.Generics.Collections,
  Model.Noticia;

type
  { Concrete Aggregate }
  TConcreteAggregateCSV = class(TInterfacedObject, IAggregate<TNoticia>)
  private
    // Lista de objetos para armazenar os clientes
    FLista: TObjectList<TNoticia>;

    function ToDate(SDate: string): TDate;
    function ToString(JSON: String): String;
    function ToMemoString(JSON: String): String;

    // Método para preencher a lista de objetos
    procedure PreencherLista(const CaminhoArquivo: string);
    procedure OrdenarLista;
  public
    constructor Create(const CaminhoArquivo: string);
    destructor Destroy; override;

    function GetLista: TObjectList<TNoticia>;
    function GetIterator: IIterator<TNoticia>;
  end;

implementation

uses
  System.Classes, System.SysUtils, Pattern.ConcreteIterator,
  System.DateUtils, System.JSON, Data.DBXJSON, System.Generics.Defaults;

{ TConcreteAggregateCSV }

constructor TConcreteAggregateCSV.Create(const CaminhoArquivo: string);
begin
  // Cria a lista de objetos
  FLista := TObjectList<TNoticia>.Create;

  // Preenche a lista de objetos
  PreencherLista(CaminhoArquivo);
  OrdenarLista;
end;

destructor TConcreteAggregateCSV.Destroy;
begin
  // Libera a lista de objetos da memória
  FLista.Free;
  inherited;
end;

function TConcreteAggregateCSV.ToDate(SDate: string): TDate;
begin
  Result := EncodeDate(
    SDate.Substring(6, 4).ToInteger,
    SDate.Substring(3, 2).ToInteger,
    SDate.Substring(0, 2).ToInteger
  );
end;

function TConcreteAggregateCSV.ToMemoString(JSON: String): String;
var
  ArrayDados: TJSONArray;
  aJSON: TJSONValue;
  aStringList: TStrings;
begin
  Result := '';
  aStringList := TStringList.Create;
  try
    ArrayDados := TJSONObject.ParseJSONValue(TEncoding.UTF8.GetBytes(JSON), 0) as TJSONArray;
    for aJSON in ArrayDados do
    begin
      if not aJSON.Value.Trim.IsEmpty then
        aStringList.Add(aJSON.Value.Trim)
    end;

    Result := Result + String.Join(sLineBreak, aStringList.ToStringArray);
  finally
    aStringList.Free;
  end;
end;

function TConcreteAggregateCSV.ToString(JSON: String): String;
var
  ArrayDados: TJSONArray;
  aJSON: TJSONValue;
begin
  Result := '';
  ArrayDados := TJSONObject.ParseJSONValue(TEncoding.UTF8.GetBytes(JSON), 0) as TJSONArray;
  for aJSON in ArrayDados do
  begin
    Result := Result + aJSON.Value;
  end;
  Result := Result.Trim;
end;

function TConcreteAggregateCSV.GetIterator: IIterator<TNoticia>;
begin
  Result := TConcreteIterator.Create(Self);
end;

function TConcreteAggregateCSV.GetLista: TObjectList<TNoticia>;
begin
  Result := FLista;
end;

procedure TConcreteAggregateCSV.OrdenarLista;
var
  Comparison: TComparison<TNoticia>;
begin
  Comparison :=
    function(const Left, Right: TNoticia): Integer
    begin
      Result := CompareDate(Left.DataAtualizacao, Right.DataAtualizacao);
    end;

  FLista.Sort(TComparer<TNoticia>.Construct(Comparison));
end;

procedure TConcreteAggregateCSV.PreencherLista(const CaminhoArquivo: string);
var
  aNoticia: TNoticia;
  Valores: TStringList;
  JSON: TJSONObject;
  ArrayDados: TJSONArray;
  Contador: integer;
begin
  // Cria a TStringList que irá carregar o arquivo selecionado
  Valores := TStringList.Create;
  try
    // Carrega o arquivo
    Valores.LoadFromFile(CaminhoArquivo);

    // Seleciona o array "dados" do JSON
    ArrayDados := TJSONObject.ParseJSONValue(TEncoding.UTF8.GetBytes(Valores.Text),0) as TJSONArray;

    // Executa um loop nos itens do array
    for Contador := 0 to Pred(ArrayDados.Count) do
    begin
      // Converte o item atual do array para um objeto JSON
      JSON := ArrayDados.Items[Contador] as TJSONObject;

      aNoticia := TNoticia.Create;

      aNoticia.Conteudo := UTF8ToAnsi(ToMemoString(JSON.Values['conteudo'].ToString)); // JSON.Values['conteudo'].ToString);
      aNoticia.DataAtualizacao := ToDate(ToString(JSON.Values['data_atualizacao'].ToString));
      aNoticia.Titulo := UTF8ToAnsi(ToString(JSON.Values['titulo'].ToString));
      try
        aNoticia.Sentimento := senNeutro;
        if JSON.ToJSON.Contains('sentimento') then
        begin
          if JSON.Values['sentimento'].ToString.Trim = '-1' then
            aNoticia.Sentimento := senNegativo
          else if JSON.Values['sentimento'].ToString.Trim = '0' then
            aNoticia.Sentimento := senNeutro
          else aNoticia.Sentimento := senPositivo
        end;
      except
        aNoticia.Sentimento := senNegativo;
      end;


      // Adiciona o objeto na lista
      FLista.Add(aNoticia);
    end;
  finally
    // Libera a variável da memória
    FreeAndNil(Valores);
  end;
end;

end.
