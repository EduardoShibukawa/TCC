unit Pattern.ConcreteAggregateJSON;

interface

uses
  Pattern.Iterator, Pattern.Aggregate, Contnrs, System.Generics.Collections,
  Model.Noticia;

type
  { Concrete Aggregate }
  TConcreteAggregateJSON = class(TInterfacedObject, IAggregate<TNoticia>)
  private
    // Lista de objetos para armazenar os clientes
    FLista: TObjectList<TNoticia>;

    function ToDate(SDate: string): TDate;
    function ToString(JSON: String): String;
    function ToMemoString(JSON: String): String;

    // Método para preencher a lista de objetos
    procedure PreencherListaJSONScrapyHub(const CaminhoArquivo: string);
    procedure PreencherListaJSONNormal(const CaminhoArquivo: string);
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

constructor TConcreteAggregateJSON.Create(const CaminhoArquivo: string);
begin
  FLista := TObjectList<TNoticia>.Create;
  try
    PreencherListaJSONScrapyHub(CaminhoArquivo);
  except
    PreencherListaJSONNormal(CaminhoArquivo);
  end;
  OrdenarLista;
end;

destructor TConcreteAggregateJSON.Destroy;
begin
  // Libera a lista de objetos da memória
  FLista.Free;
  inherited;
end;

function TConcreteAggregateJSON.ToDate(SDate: string): TDate;
begin
  Result := EncodeDate(
    SDate.Substring(6, 4).ToInteger,
    SDate.Substring(3, 2).ToInteger,
    SDate.Substring(0, 2).ToInteger
  );
end;

function TConcreteAggregateJSON.ToMemoString(JSON: String): String;
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

function TConcreteAggregateJSON.ToString(JSON: String): String;
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

function TConcreteAggregateJSON.GetIterator: IIterator<TNoticia>;
begin
  Result := TConcreteIterator.Create(Self);
end;

function TConcreteAggregateJSON.GetLista: TObjectList<TNoticia>;
begin
  Result := FLista;
end;

procedure TConcreteAggregateJSON.OrdenarLista;
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

procedure TConcreteAggregateJSON.PreencherListaJSONNormal(const CaminhoArquivo: string);
var
  aNoticia: TNoticia;
  aValores: TStringList;
  aJSON: TJSONObject;
  ArrayDados: TJSONArray;
  aContador: Integer;
begin
  // Cria a TStringList que irá carregar o arquivo selecionado
  aValores := TStringList.Create;
  try
    // Carrega o arquivo
    aValores.LoadFromFile(CaminhoArquivo);

    // Seleciona o array "dados" do JSON
    ArrayDados := TJSONObject.ParseJSONValue(TEncoding.UTF8.GetBytes(aValores.Text),0) as TJSONArray;

    // Executa um loop nos itens do array
    for aContador := 0 to Pred(ArrayDados.Count) do
    begin
      // Converte o item atual do array para um objeto JSON
      aJSON := ArrayDados.Items[aContador] as TJSONObject;

      aNoticia := TNoticia.Create;

      aNoticia.Conteudo := UTF8ToAnsi(aJSON.GetValue<string>('conteudo')); // JSON.Values['conteudo'].ToString);
      aNoticia.DataAtualizacao := ToDate(aJSON.GetValue<string>('data_atualizacao'));
      aNoticia.Titulo := UTF8ToAnsi(aJSON.GetValue<string>('titulo'));
      try
        aNoticia.Sentimento := senNeutro;
        if aJSON.ToJSON.Contains('sentimento') then
        begin
          if aJSON.GetValue<string>('sentimento').Trim() = '-1' then
            aNoticia.Sentimento := senNegativo
          else if aJSON.GetValue<string>('sentimento').Trim() = '0' then
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
    FreeAndNil(aValores);
  end;
end;

procedure TConcreteAggregateJSON.PreencherListaJSONScrapyHub(const CaminhoArquivo: string);
var
  aNoticia: TNoticia;
  aValores: TStringList;
  aJSON: TJSONObject;
  ArrayDados: TJSONArray;
  aContador: integer;
begin
  aValores := TStringList.Create;
  try
    aValores.LoadFromFile(CaminhoArquivo);

    ArrayDados := TJSONObject.ParseJSONValue(TEncoding.UTF8.GetBytes(aValores.Text),0) as TJSONArray;

    for aContador := 0 to Pred(ArrayDados.Count) do
    begin
      aJSON := ArrayDados.Items[aContador] as TJSONObject;

      aNoticia := TNoticia.Create;

      aNoticia.Conteudo := UTF8ToAnsi(ToMemoString(aJSON.Values['conteudo'].ToString));
      aNoticia.DataAtualizacao := ToDate(ToString(aJSON.Values['data_atualizacao'].ToString));
      aNoticia.Titulo := UTF8ToAnsi(ToString(aJSON.Values['titulo'].ToString));
      try
        aNoticia.Sentimento := senNeutro;
        if aJSON.ToJSON.Contains('sentimento') then
        begin
          if aJSON.Values['sentimento'].ToString.Trim = '-1' then
            aNoticia.Sentimento := senNegativo
          else if aJSON.Values['sentimento'].ToString.Trim = '0' then
            aNoticia.Sentimento := senNeutro
          else aNoticia.Sentimento := senPositivo
        end;
      except
        aNoticia.Sentimento := senNegativo;
      end;

      FLista.Add(aNoticia);
    end;
  finally
    FreeAndNil(aValores);
  end;
end;

end.
