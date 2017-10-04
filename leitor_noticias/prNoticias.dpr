program prNoticias;

uses
  Vcl.Forms,
  View.Noticias in 'View\View.Noticias.pas' {fNoticias},
  Pattern.Aggregate in 'Pattern\Pattern.Aggregate.pas',
  Pattern.ConcreteAggregateCSV in 'Pattern\Pattern.ConcreteAggregateCSV.pas',
  Pattern.Iterator in 'Pattern\Pattern.Iterator.pas',
  Model.Noticia in 'Model\Model.Noticia.pas',
  Pattern.Abstraction in 'Pattern\Pattern.Abstraction.pas',
  Pattern.Implementor in 'Pattern\Pattern.Implementor.pas',
  Pattern.RefinedAbstraction.Noticia in 'Pattern\Pattern.RefinedAbstraction.Noticia.pas',
  Pattern.ConcreteImplementorCSV in 'Pattern\Pattern.ConcreteImplementorCSV.pas',
  Pattern.ConcreteIterator in 'Pattern\Pattern.ConcreteIterator.pas';

{$R *.res}

begin
  Application.Initialize;
  Application.MainFormOnTaskbar := True;
  Application.CreateForm(TfNoticias, fNoticias);
  Application.Run;
end.
